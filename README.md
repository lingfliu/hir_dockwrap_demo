## 算法类服务Http封装
### 项目结构
1. api: 第三方api接口（文件读写，结果更新等）
2. service: http service wrapper
3. infer: inference service (算法推理服务，见代码内注释)
4. Dockerfile: dockerfile for building docker image
5. environment.yml: conda environment file exported using ```conda env export > environment.yml```
6. docker.sh: build docker image and run docker container

### 待修改部分：
1. docker基础镜像应当选用含cuda的镜像，否则无法使用GPU 
2. docker未测试
3. 未集成k8s编排，待第三方软件团队提供
