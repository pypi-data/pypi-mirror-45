import subprocess
import re
import os
import json
import csv

model_share = '\\\\redmond\\1windows\\TestContent\\CORE\\SiGMa\\GRFX\\WinML\\19H1\\models\\'

img_share = '\\\\redmond\\1windows\\TestContent\\CORE\\SiGMa\\GRFX\\WinML\\input_data\\ImageNet_224'

#models = ['onnxzoo_lotus_vgg19', 'squeezenet1.1', 'resnet50v1', 'coreml_inceptionv3_imagenet​']
models = ['resnet50v1', 'coreml_inceptionv3_imagenet​']

def read_image_label(filePath):
    img_labels = {}
    with open(filePath, 'r') as file:
        for line in file.readlines():
            image, _, label = line.replace('\n','').split(' ')
            img_labels[image] = label
    return img_labels

def read_index_label(filePath):
    index_labels = {}
    with open(filePath, 'r') as file:
        index_labels = json.loads(file.read().replace('\n', ' '))
    return index_labels


def get_topk_accuracy(model_path, k, img_path, img_labels, index_labels, csv_writer):
    # call winmlrunner
    cmd = ['WinMLRunner.exe', '-model', model_path, '-input', img_path, '-cpu', '-topK', str(k)]
    result = subprocess.check_output(cmd)
    lines = str(result).split(r'\r\n')
    # lines swill contain strings of index values pair.
    # e.g) ['index: 409, value: 6.74914', 'index: 769, value: 5.66233', ' index: 664, value: 5.62002']
    lines = list(filter(lambda x: 'index:' in x, lines))
    img_base_path = os.path.basename(img_path)
    img_name = re.match('n[0-9]+', img_base_path).group(0)
    actual_label = img_labels[img_name]
    print('testing {}'.format(img_base_path))
    predicted_labels = []
    predicted_values = []
    for line in lines:
        index, value = re.findall('[0-9.]+[e-]*[0-9]*', line)
        cur_label = index_labels[index]
        predicted_labels.append(cur_label)
        predicted_values.append(value)
    if actual_label in ''.join(predicted_labels):
        matched = True
        is_matched = 'Success'
    else:
        matched = False
        is_matched = 'Fail'
    first_row = [img_base_path, actual_label, is_matched] + predicted_labels
    second_row = ['','',''] + predicted_values
    
    csv_writer.writerow(first_row)
    # at the end of first row print success if in top k fail else
    csv_writer.writerow(second_row)
    return matched
    

def get_accuracy(model_path, k):
    model_name = os.path.splitext(os.path.basename(model_path))[-2]
    print('testing model {}'.format(model_name))
    with open(model_name + '-accuracy.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        img_labels = read_image_label('true-label.txt')
        index_labels = read_index_label('labels.json')
        total = 0
        matched = 0
        for img_name in os.listdir(img_share):
            img = img_share + '\\' + img_name
            if re.match('n[0-9]+', img_name) is None:
                print('skipping image ' + img_name)
                continue
            if get_topk_accuracy(model_path, k, img, img_labels, index_labels, csv_writer):
                matched += 1
            total += 1
        csv_writer.writerow(['Matched', str(matched)])
        csv_writer.writerow(['Total', str(total)])

def get_perf(model_path, iterations):
    model_name = os.path.splitext(os.path.basename(model_path))[-2]
    print('getting perf model {}'.format(model_name))
    with open(model_name + '-perf.csv', 'w', newline='') as csv_file:
        cmd = ['WinMLRunner.exe', '-model', model_path, '-perf', '-iterations', '100']


if __name__ == '__main__':
    for model in models:
        og_name = model_share + '\\onnx-1.3\\' + model + '.onnx'
        quantized_name = model_share + '\\quantization\\' + model + '-dq.onnx'
        get_accuracy(og_name, 5)
        get_accuracy(quantized_name, 5)

