# Gradio

`Gradio` is a python library that allows you to place input and output interfaces over trained models to make it easy for you to "play around" with your model. Gradio runs entirely locally using your browser.

To get a sense of `gradio`, take a look at the  python notebooks in the `examples` folder, or read on below! And be sure to visit the gradio website: www.gradio.app.

## Installation
```
pip install gradio
```
(you may need to replace `pip` with `pip3` if you're running `python3`).

## Usage

Gradio is very easy to use with your existing code. Here is a minimum working example:


```python
import gradio
import tensorflow as tf
image_mdl = tf.keras.applications.inception_v3.InceptionV3()

io = gradio.Interface(inputs="imageupload", outputs="label", model_type="keras", model=image_mdl)
io.launch()
```

You can supply your own model instead of the pretrained model above, as well as use different kinds of models, not just keras models. Changing the `input` and `output` parameters in the `Interface` face object allow you to create different interfaces, depending on the needs of your model. Take a look at the python notebooks for more examples. The currently supported interfaces are as follows:

**Input interfaces**:
* Sketchpad
* ImageUplaod
* Webcam
* Textbox

**Output interfaces**:
* Label
* Textbox

## Screenshots

Here are a few screenshots that show examples of gradio interfaces

#### MNIST Digit Recognition (Input: Sketchpad, Output: Label)

```python
iface = gradio.Interface(input='sketchpad', output='label', model=model, model_type='keras')
iface.launch()
```

![alt text](https://raw.githubusercontent.com/abidlabs/gradio/master/screenshots/mnist4.png)

#### Facial Emotion Detector (Input: Webcam, Output: Label)

```python
iface = gradio.Interface(inputs='webcam', outputs='label', model=model, model_type='keras')
iface.launch()
```

![alt text](https://raw.githubusercontent.com/abidlabs/gradio/master/screenshots/webcam_happy.png)

#### Sentiment Analysis (Input: Textbox, Output: Label)

```python
iface = gradio.Interface(inputs='textbox', outputs='label', model=model, model_type='keras')
iface.launch()
```

![alt text](https://raw.githubusercontent.com/abidlabs/gradio/master/screenshots/sentiment_positive.png)

### More Documentation

More detailed and up-to-date documentation can be found on the gradio website: www.gradio.app.


