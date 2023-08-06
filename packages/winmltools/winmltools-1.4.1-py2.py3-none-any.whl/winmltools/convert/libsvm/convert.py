#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------

from ...proto import onnx_proto
from ..common import get_converter
from ..common import ModelBuilder
from ..common import model_util
from .SVMConvertContext import SVMConvertContext as ConvertContext

from onnxmltools.convert.common.data_types import *
import sklearn.pipeline as pipeline

# These are not referenced directly but are imported
# to initialize the registration call
from .SVMConverter import AnyLibSvmConverter

def convert(model, name=None, initial_types=None):
    if isinstance(model, str):
        # model is a path name
        model = _load_model(model)

    context = ConvertContext()
    inputs = [model_util.make_tensor_value_info(context.get_unique_name('Input'), onnx_proto.TensorProto.FLOAT)]
    if initial_types:
        inputs = []
        try:
            for input_name, input_type in initial_types:
                input_shape = input_type.shape
                if isinstance(input_type, (Int64TensorType, Int64Type)):
                    elem_type = model_util.tensorproto_typemap['int64']
                elif isinstance(input_type, (FloatTensorType, FloatType)):
                    elem_type = model_util.tensorproto_typemap['float']
                elif isinstance(input_type, (StringTensorType, StringType)):
                    elem_type = model_util.tensorproto_typemap['string']
                else:
                    raise RuntimeError('Unknown input type')
                inputs.append(model_util.make_tensor_value_info(context.get_unique_name(input_name),
                                                                elem_type, input_shape))
            if len(initial_types) > 1:
                nodes.append(_create_feature_vectorizer_node(context, inputs))
                inputs = nodes[-1].outputs
        except:
            raise ValueError('Invalid initial_types argument.')
    else:
        raise ValueError('Specify model input names and  types when calling this convert(...) function')
    
    converter = get_converter(type(model))
    onnx_nodes = []

    outputs = None
    converter.validate(model)

    nodes = converter.convert(context, model, inputs)
    mb = ModelBuilder(name)
    for node in nodes:
        mb.add_nodes([node.onnx_node])
        mb.add_initializers(node.initializers)
        mb.add_values(node.values)
        mb.add_domain_version_pair(node.domain_version_pair)
    mb.add_inputs(inputs)
    mb.add_outputs(nodes[-1].outputs)
    return mb.make_model()


def _load_model(model_path):
    try:
        import svmutil
    except ImportError:
        raise ImportError("svmutil is required to load the model trained with libsvm.")
    return svmutil.load_model(model_path)
