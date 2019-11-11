import base64
import logging
from io import BytesIO

from torch.utils.data import DataLoader

from api.api_utils import Timer
from pytorch_yolov3.models import *
from pytorch_yolov3.utils.datasets import *
from pytorch_yolov3.utils.utils import *


class Base64Source(Dataset):
    def __init__(self, b64_images, img_size=416):
        self.images = {name: Image.open(BytesIO(base64.b64decode(b64))) for name, b64 in b64_images.items()}
        self.img_size = img_size

    def __getitem__(self, index):
        name = list(self.images.keys())[index % len(self.images)]
        # Extract image as PyTorch tensor
        img = transforms.ToTensor()(self.images[name])
        # Pad to square resolution
        img, _ = pad_to_square(img, 0)
        # Resize
        img = resize(img, self.img_size)

        return name, img

    def __len__(self):
        return len(self.images.keys())


class PredictionHandler:
    logger = logging.getLogger(__name__)

    def __init__(self, options) -> None:
        self.opt = options
        self.model = self.init_model()

    def init_model(self):
        device_type = "cuda" if torch.cuda.is_available() else "cpu"
        self.logger.info(f"Initializing model on {device_type}")
        device = torch.device(device_type)

        # Set up model
        model = Darknet(self.opt.model_def, img_size=self.opt.img_size).to(device)

        if self.opt.weights_path.endswith(".weights"):
            # Load darknet weights
            model.load_darknet_weights(self.opt.weights_path)
        else:
            # Load checkpoint weights
            model.load_state_dict(torch.load(self.opt.weights_path))

        model.eval()  # Set in evaluation mode
        return model

    def predict(self, request_data):
        res = {}
        timer = Timer()
        with timer("total"):
            source = Base64Source(request_data, img_size=self.opt.img_size)
            dataloader = DataLoader(
                source,
                batch_size=self.opt.batch_size,
                shuffle=False,
                num_workers=self.opt.n_cpu,
            )

            classes = load_classes(self.opt.class_path)  # Extracts class labels from file

            Tensor = torch.cuda.FloatTensor if torch.cuda.is_available() else torch.FloatTensor

            for batch_i, (img_sources, input_imgs) in enumerate(dataloader):
                with timer(f"batch_{batch_i}"):
                    input_imgs = Variable(input_imgs.type(Tensor))

                    with timer("predict"):
                        with torch.no_grad():
                            detections = self.model(input_imgs)
                            detections = non_max_suppression(detections, self.opt.conf_thres, self.opt.nms_thres)

                    for img_source, d in zip(img_sources, detections):
                        source_res = res.setdefault(img_source, [])
                        if d is None:
                            continue
                        img_objects = rescale_boxes(d, self.opt.img_size, source.images[img_source].size[::-1])
                        for x1, y1, x2, y2, conf, cls_conf, cls_pred in img_objects:
                            source_res.append({"x1": x1.item(),
                                               "y1": y1.item(),
                                               "x2": x2.item(),
                                               "y2": y2.item(),
                                               "conf": conf.item(),
                                               "cls_conf": cls_conf.item(),
                                               "cls_pred": classes[int(cls_pred)]})

        return {"timing": timer.intervals, "result": res}
