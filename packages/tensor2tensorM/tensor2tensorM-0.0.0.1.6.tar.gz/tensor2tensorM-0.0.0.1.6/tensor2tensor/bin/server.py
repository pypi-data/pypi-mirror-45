from flask import Flask
from tensor2tensor.bin.t2t_gendata import router_datagen


from tensor2tensor.bin.t2t_train import router_train
from tensor2tensor.bin.router_synthesize import router_synthesize
def main(_):
    app = Flask(__name__)
    app.register_blueprint(router_datagen)
    app.register_blueprint(router_train)
    app.register_blueprint(router_synthesize)
    app.run(debug=True, host='0.0.0.0', port=8891)



if __name__ == "__main__":
    main()

    # modality, jax, jaxlib, kfac, pypng, tensorflow-datasets


#falcon==1.2.0
#inflect==0.2.5
#audioread==2.1.5
#librosa==0.5.1
#matplotlib==2.0.2
#numpy==1.14.0
#scipy==1.0.0
#tqdm==4.11.2
#Unidecode==0.4.20
#pyaudio==0.2.11
#sounddevice==0.3.10
#lws
#keras
#flask
#tensorflow
#easydict


#numpy
#librosa
#tensorflow
#matplotlib
#tqdm
#pyaudio
#sounddevice
#unidecode
#inflect
#keras
#easydict
#flask
