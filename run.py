import argparse
import logging.config

logging.config.fileConfig("logging.conf")

if __name__ == '__main__':
    from api.endpoints import create_restyolo_api

    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5000, help="REST api port")
    parser.add_argument("--model_def", type=str, default="pytorch_yolov3/config/yolov3-tiny.cfg",
                        help="path to model definition file")
    parser.add_argument("--weights_path", type=str, default="pytorch_yolov3/weights/yolov3-tiny.weights",
                        help="path to weights file")
    parser.add_argument("--class_path", type=str, default="pytorch_yolov3/data/coco.names",
                        help="path to class label file")
    parser.add_argument("--conf_thres", type=float, default=0.8, help="object confidence threshold")
    parser.add_argument("--nms_thres", type=float, default=0.4, help="iou thresshold for non-maximum suppression")
    parser.add_argument("--batch_size", type=int, default=5, help="size of the batches")
    parser.add_argument("--n_cpu", type=int, default=0, help="number of cpu threads to use during batch generation")
    parser.add_argument("--img_size", type=int, default=416, help="size of each image dimension")

    opt = parser.parse_args()
    logger.info("Creating API")
    app = create_restyolo_api(opt)

    logger.info(f"{'#' * 5} Starting server on port {opt.port} {'#' * 5}")
    app.run(host='0.0.0.0', port=opt.port)
