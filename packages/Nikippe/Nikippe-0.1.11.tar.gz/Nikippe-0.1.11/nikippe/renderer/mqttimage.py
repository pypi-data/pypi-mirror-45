from io import BytesIO
from nikippe.renderer.aelementmqtt import AElementMQTT
from PIL import Image, ImageChops


class MQTTImage(AElementMQTT):
    """
    Displays images that are received via mqtt messages. Until first received image, background-color is used. If an
    empty message is received - background-color will be displayed again.

    The image must be sent as ```bytes```. Thus, the sender must implement something like:
        bytes_image = BytesIO()
        image.save(bytes_image, format="png")
        mqtt_message = bytes_image.getvalue()

    additional yaml entries:
      offset_x - offset for image within element plane (optional, default=0)
      offset_y - offset for image within element plane (optional, default=0)
    """
    _mqtt_image = None
    _offset_x = None
    _offset_y = None

    def __init__(self, config, update_available, mqtt_client, logger):
        AElementMQTT.__init__(self, config, update_available, mqtt_client, logger, self.__class__.__name__)

        try:
            self._offset_x = self._config["offset_x"]
        except KeyError:
            self._offset_x = 0
        try:
            self._offset_y = self._config["offset_y"]
        except KeyError:
            self._offset_y = 0

    def _topic_sub_handler(self, value):
        self._logger.info("MQTTImage._topic_sub_handler - received value '{}'.".format(value))
        if len(value) == 0:
            self._logger.debug("MQTTImage._topic_sub_handler - recevied empty message -> background-color image is "
                              "displayed.")
            self._mqtt_image = None
            self._set_update_available()
        else:
            self._logger.debug("MQTTImage._topic_sub_handler - received image")
            try:
                self._mqtt_image = Image.open(BytesIO(value))
            except SyntaxError as e:
                self._logger.error("MQTTImage._topic_sub_handler - SyntaxError: {}".format(e))
                return

            self._mqtt_image = self._mqtt_image.convert("L")
            self._set_update_available()

    def _start(self):
        pass

    def _stop(self):
        pass

    def _update_image(self):
        self._logger.info("MQTTImage.updateImage()")
        if self._mqtt_image is not None:
            try:
                # clear result image
                self.img = ImageChops.constant(self.img, self._background_color)
                # place static image
                self.img.paste(self._mqtt_image, box=(self._offset_x, self._offset_y))
            except SyntaxError as e:
                self._logger.error(e)


