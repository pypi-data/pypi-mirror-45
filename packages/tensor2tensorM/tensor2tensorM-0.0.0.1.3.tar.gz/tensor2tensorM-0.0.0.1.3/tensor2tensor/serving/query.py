# coding=utf-8
# Copyright 2019 The Tensor2Tensor Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Query an exported model. Py2 only. Install tensorflow-serving-api."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from oauth2client.client import GoogleCredentials
from six.moves import input  # pylint: disable=redefined-builtin

from tensor2tensor import problems as problems_lib  # pylint: disable=unused-import
from tensor2tensor.serving import serving_utils
from tensor2tensor.utils import registry
from tensor2tensor.utils import usr_dir
from tensor2tensor.utils.hparam import HParams
import tensorflow as tf
from tensor2tensor import problems
from tensor2tensor.utils import trainer_lib

from tensorflow.contrib.eager.python import tfe
tfe = tf.contrib.eager
tfe.enable_eager_execution()
Modes = tf.estimator.ModeKeys

flags = tf.flags
FLAGS = flags.FLAGS

flags.DEFINE_string("server", None, "Address to Tensorflow Serving server.")
flags.DEFINE_string("servable_name", None, "Name of served model.")
flags.DEFINE_string("problem", None, "Problem name.")
flags.DEFINE_string("data_dir", None, "Data directory, for vocab files.")
flags.DEFINE_string("t2t_usr_dir", None, "Usr dir for registrations.")
flags.DEFINE_string("inputs_once", None, "Query once with this input.")
flags.DEFINE_integer("timeout_secs", 10, "Timeout for query.")

# For Cloud ML Engine predictions.
flags.DEFINE_string("cloud_mlengine_model_name", None,
                    "Name of model deployed on Cloud ML Engine.")
flags.DEFINE_string(
    "cloud_mlengine_model_version", None,
    "Version of the model to use. If None, requests will be "
    "sent to the default version.")


def validate_flags():
  """Validates flags are set to acceptable values."""
  if FLAGS.cloud_mlengine_model_name:
    assert not FLAGS.server
    assert not FLAGS.servable_name
  else:
    assert FLAGS.server
    assert FLAGS.servable_name


def make_request_fn():
  """Returns a request function."""
  if FLAGS.cloud_mlengine_model_name:
    request_fn = serving_utils.make_cloud_mlengine_request_fn(
        credentials=GoogleCredentials.get_application_default(),
        model_name=FLAGS.cloud_mlengine_model_name,
        version=FLAGS.cloud_mlengine_model_version)
  else:

    request_fn = serving_utils.make_grpc_request_fn(
        servable_name=FLAGS.servable_name,
        server=FLAGS.server,
        timeout_secs=FLAGS.timeout_secs)
  return request_fn


def main(_):
  tf.logging.set_verbosity(tf.logging.INFO)
  # validate_flags()




  values = {
	"data_dir":"/mnt/disks/mnt-dir/t2t_tmp/data/",
	"checkpoint_dir": "/home/manuel_garcia02/checkpoint",
	"problem_name": "deepspeech",
	"file": "audio1",
	"dir_file": "/home/manuel_garcia02"
}

  data_dir = values['data_dir']
  checkpoint_dir = values['checkpoint_dir']
  # usr_dir = "/home/manuel_garcia02/tensor2tensor/tensor2tensor/data_generators/"
  # tf.gfile.MakeDirs(data_dir)

  problem_name = values['problem_name']


  model_name = "transformer"
  hparams_set = "transformer_librispeech_tpu"
  #
  # hparams = trainer_lib.create_hparams(hparams_set, data_dir=data_dir, problem_name=problem_name)

  # usr_dir.import_usr_dir(FLAGS.t2t_usr_dir)
  problem = registry.problem(problem_name)
  hparams = HParams(data_dir=os.path.expanduser(data_dir))
  problem.get_hparams(hparams)
  trainer_lib.create_hparams(hparams_set, data_dir=data_dir, problem_name=problem_name)
  asr_problem = problems.problem(problem_name)
  encoders = asr_problem.feature_encoders(None)
  asr_model = registry.model(model_name)(hparams, Modes.PREDICT)

  request_fn = make_request_fn()

  def encode(x):
      waveforms = encoders["waveforms"].encode(x)
      encoded_dict = asr_problem.preprocess_example({"waveforms": waveforms, "targets": []}, Modes.PREDICT,
                                                    hparams)

      return {"inputs": tf.expand_dims(encoded_dict["inputs"], 0),
              "targets": tf.expand_dims(encoded_dict["targets"], 0)}





  prerecorded_messages = []
  save_filename = os.path.join(os.path.abspath(values['dir_file']), values['file'])

  prerecorded_messages.append(save_filename)

  input = ''
  output = ''



  while True:
    inputs = ''
    output = ''
    score = ''
    for inputs1 in prerecorded_messages:
        inputs = encode(inputs1)['inputs']
        outputs = serving_utils.predict([inputs], problem, request_fn)
        outputs, = outputs
        output, score = outputs
    if len(score.shape) > 0:  # pylint: disable=g-explicit-length-test
      print_str = """
Input:
{inputs}
Output (Scores [{score}]):
{output}
        """
      score_text = ",".join(["{:.3f}".format(s) for s in score])
      print(print_str.format(inputs=inputs, output=output, score=score_text))
    else:
      print_str = """
Input:
{inputs}
Output (Score {score:.3f}):
{output}
        """
      print(print_str.format(inputs=inputs, output=output, score=score))

    if FLAGS.inputs_once:
      break


if __name__ == "__main__":
  flags.mark_flags_as_required(["problem", "data_dir"])
  tf.app.run()