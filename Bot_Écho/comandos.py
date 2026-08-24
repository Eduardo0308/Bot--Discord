import tf_keras as keras  # Importando tf-keras – uma versão do Keras compatível com modelos .h5
from tf_keras.models import load_model  # Importando a função load_model do tf_keras, que permite abrir o modelo
from PIL import Image, ImageOps  # Instalando pillow no lugar do PIL
import numpy as np

def get_class(model, label, image):

  # Disable scientific notation for clarity
  np.set_printoptions(suppress=True)

  # Load the model
  model = load_model(model, compile=False)

  # Load the labels
  class_names = open(label, "r").readlines()

  image = Image.open(image).convert("RGB")

  # Create the array of the right shape to feed into the keras model
  # The 'length' or number of images you can put into the array is
  # determined by the first position in the shape tuple, in this case 1
  data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

  # resizing the image to be at least 224x224 and then cropping from the center
  size = (224, 224)
  image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

  # turn the image into a numpy array
  image_array = np.asarray(image)

  # Normalize the image
  normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

  # Load the image into the array
  data[0] = normalized_image_array

  # Predicts the model
  prediction = model.predict(data)
  index = np.argmax(prediction)
  class_name = class_names[index]
  confidence_score = prediction[0][index]

  # Print prediction and confidence score
  return class_name[2:]