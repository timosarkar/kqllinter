```bash
wget https://huggingface.co/bartowski/DeepSeek-R1-Distill-Qwen-1.5B-GGUF/blob/main/DeepSeek-R1-Distill-Qwen-1.5B-Q8_0.gguf -p models
git submodule update --init
mkdir build
cd build
cmake ..
make chat -j
./chat
```
