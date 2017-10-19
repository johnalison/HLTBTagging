import logging
import logging.config
import os
import json

def setup_logging( default_path='config/logging.json', default_level=logging.INFO,
                   logname = "output", errname = "error", loglevel = 20):
    """
    Setup logging configuration
    """
    path = default_path
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        #Overwrite config definitions with command line arguments (Default is same as in config)
        config["handlers"]["info_file_handler"]["filename"] = "logs/"+logname+".log"
        config["handlers"]["error_file_handler"]["filename"] = "logs/"+errname+".log"
        config["handlers"]["console"]["level"] = loglevel
        config["handlers"]["info_file_handler"]["level"] = loglevel
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)



def savePlot(canvas, outputname, outputformat):
    #TODO: Make something with multipage pdf support
    logging.info("Writing file {0}.{1}".format(outputname, outputformat))
    canvas.Print("{0}.{1}".format(outputname, outputformat))
