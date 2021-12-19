### Download data and preprocess

```shell
cd dataset
wget https://s3.amazonaws.com/code-search-net/CodeSearchNet/v2/python.zip

unzip python.zip
rm *.zip
rm *.pkl

python preprocess.py
rm -r */final
cd ..
```


### Data Format

After preprocessing dataset, you can obtain three .jsonl files, i.e. train.jsonl, valid.jsonl, test.jsonl

For each file, each line in the uncompressed file represents one function.  One row is illustrated below.

  - **repo:** the owner/repo

  - **path:** the full path to the original file

  - **func_name:** the function or method name

  - **original_string:** the raw string before tokenization or parsing

  - **language:** the programming language

  - **code/function:** the part of the `original_string` that is code

  - **code_tokens/function_tokens:** tokenized version of `code`

  - **docstring:** the top-level comment or docstring, if it exists in the original string

  - **docstring_tokens:** tokenized version of `docstring`

### Data Statistic

| Programming Language | Training |  Dev   |  Test  |
| :------------------- | :------: | :----: | :----: |
| Python               | 251,820  | 13,914 | 14,918 |
| PHP                  | 241,241  | 12,982 | 14,014 |
| Go                   | 167,288  |  7,325 |  8,122 |
| Java                 | 164,923  |  5,183 | 10,955 |
| JavaScript           |  58,025  |  3,885 |  3,291 |
| Ruby                 |  24,927  |  1,400 |  1,261 |


### Dependency

- python 3.6 or 3.7
- torch==1.4.0
- transformers>=2.5.0

### Fine-tune

To fine-tune encoder-decoder on the dataset

```shell
cd code
lang=python
lr=5e-5
batch_size=8
beam_size=10
source_length=64
target_length=64
data_dir=../dataset
output_dir=model/$lang
train_file=$data_dir/$lang/train.jsonl
dev_file=$data_dir/$lang/valid.jsonl
epochs=10 
pretrained_model=roberta-base

python run.py --do_train --do_eval --model_type roberta --model_name_or_path $pretrained_model --train_filename $train_file --dev_filename $dev_file --output_dir $output_dir --max_source_length $source_length --max_target_length $target_length --beam_size $beam_size --train_batch_size $batch_size --eval_batch_size $batch_size --learning_rate $lr --num_train_epochs $epochs
```


### Inference

```shell
batch_size=8
dev_file=$data_dir/$lang/valid.jsonl
test_file=$data_dir/$lang/test.jsonl
test_model=$output_dir/checkpoint-best-bleu/pytorch_model.bin

python run.py --do_test --model_type roberta --model_name_or_path roberta-base --load_model_path $test_model --dev_filename $dev_file --test_filename $test_file --output_dir $output_dir --max_source_length $source_length --max_target_length $target_length --beam_size $beam_size --eval_batch_size $batch_size
```
