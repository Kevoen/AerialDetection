## MMDetection代码框架
- `configs`: 网络组件结构等配置信息
- `tools`: 训练和测试的最终包装和一些实用脚本
- `mmdet`:<br>
    - `apis`: 分布式环境设定(1.x,2.0移植到mmcv),推断,测试,训练基础代码
    - `core`: anchor生成,bbox,mask编解码,变换,标签锚定,采样等,模型评估,加速,优化器，后处理等
    - `datasets`: coco,voc等数据类,数据pipelines的统一格式,数据增强，数据采样
    - `models`: 模型组件(backbone,head,loss,neck)，采用注册和组合构建的形式完成模型搭建
    - `ops`: 优化加速代码,包括nms,roialign,dcn,masked_conv，focal_loss等