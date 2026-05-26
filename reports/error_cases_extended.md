# 错误案例摘录（自动提取）

## 模型：glm-5.1

### 类型：normal

- id: normal_003
  - text: 收到录用通知后，我整个人都轻松了。
  - context: 求职成功
  - gold: positive
  - prediction: neutral
  - raw_output: >
    1.  **分析输入**：
        *   文本：收到录用通知后，我整个人都轻松了。
        *   上下文：求职成功
    2.  **理解语义**：
        *   “收到录用通知”对应上下文“求职成功”。
        *   “整个人

- id: normal_005
  - text: 新项目推进顺利，让我很有干劲。
  - context: 工作进展好
  - gold: positive
  - prediction: neutral
  - raw_output: >
    1.  **分析输入**：
        *   文本：新项目推进顺利，让我很有干劲。
        *   上下文：工作进展好
    2.  **理解语义**：
        *   文本字面意思：新项目推进顺利，让人感到有动力、有干

- id: normal_009
  - text: 收到朋友的祝福，今天心情格外好。
  - context: 朋友祝福
  - gold: positive
  - prediction: neutral
  - raw_output: >
    1.  **Analyze the Request:**
        *   Task: Determine the true emotional sentiment of the given text, considering the context.
        *   Input Text: "收到朋友的祝福，今天心情格外好。" (Received blessings from a friend, feeling exceptionally good today.)
        *   Input Context: "

- id: normal_010
  - text: 项目被退回修改，我有点沮丧。
  - context: 工作受挫
  - gold: negative
  - prediction: neutral
  - raw_output: >
    1.  **分析输入**：
        *   文本：项目被退回修改，我有点沮丧。
        *   上下文：工作受挫
    2.  **理解语义**：
        *   文本明确表达了“项目被退回修改”（负面事件）和“我有点

- id: normal_011
  - text: 手机又坏了，真让人烦。
  - context: 设备故障
  - gold: negative
  - prediction: neutral
  - raw_output: >
    1.  **分析输入**：
        *   文本：手机又坏了，真让人烦。
        *   上下文：设备故障
    2.  **理解语义**：
        *   “手机又坏了”表示遇到了设备故障，这是一个负面的客观事件。
        *   “真

### 类型：metaphor

- id: metaphor_002
  - text: 那句鼓励像一盏灯，照亮了我的路。
  - context: 被鼓励
  - gold: positive
  - prediction: neutral
  - raw_output: >
    1.  **Analyze the Request:**
        *   Task: Determine the true emotional sentiment of the given text combined with its context.
        *   Input: Text ("那句鼓励像一盏灯，照亮了我的路。") and Context ("被鼓励").
        *   Output: Exactly one label from:

- id: metaphor_003
  - text: 他的支持像一阵顺风，把我推向前方。
  - context: 支持带来帮助
  - gold: positive
  - prediction: neutral
  - raw_output: >
    1.  **Analyze the Request:**
        *   Task: Determine the true emotional sentiment of the given text combined with its context.
        *   Input Text: "他的支持像一阵顺风，把我推向前方。" (His support is like a tailwind, pushing me forward.)
        *   Input

- id: metaphor_005
  - text: 老师的点评像一把钥匙，帮我找到了答案。
  - context: 学习突破
  - gold: positive
  - prediction: neutral
  - raw_output: >
    1.  **Analyze the Request:**
        *   Task: Determine the true emotional sentiment of the text combined with its context.
        *   Input Text: "老师的点评像一把钥匙，帮我找到了答案。" (The teacher's comment was like a key, helping me find the answer.)
        *

- id: metaphor_006
  - text: 团队合作像一条顺流的河。
  - context: 协作顺畅
  - gold: positive
  - prediction: neutral
  - raw_output: >
    1.  **Analyze the Request:**
        *   Task: Determine the true emotional sentiment of the given text combined with its context.
        *   Input Text: "团队合作像一条顺流的河。" (Teamwork is like a river flowing downstream/smoothly.)
        *   Input Context: "协作

- id: metaphor_007
  - text: 她的话让整个房间亮了一下。
  - context: 情绪被点亮
  - gold: positive
  - prediction: neutral
  - raw_output: >
    1.  **Analyze the Request:**
        *   Task: Determine the true emotional sentiment of the given text combined with its context.
        *   Input Text: "她的话让整个房间亮了一下。" (Her words made the whole room light up for a moment.)
        *   Input Context: "

### 类型：sarcasm

- id: sarcasm_001
  - text: 谢谢你哈🙂，让我等了两个小时。
  - context: 用户在吐槽客服迟到
  - gold: negative
  - prediction: neutral
  - raw_output: >
    1.  **Analyze the Request:**
        *   Task: Determine the true emotion/sentiment of the given text based on the text and its context.
        *   Input Text: "谢谢你哈🙂，让我等了两个小时。" (Thank you 🙂, making me wait for two hours.)
        *

- id: sarcasm_002
  - text: 你可真会照顾人。
  - context: 朋友忘了帮忙
  - gold: negative
  - prediction: positive
  - raw_output: >
    1.  **Analyze the Request:**
        *   Task: Determine the true emotional sentiment of a text given its context.
        *   Input: Text ("你可真会照顾人。") and Context ("朋友忘了帮忙").
        *   Output: Exactly one label from: positive, neutral, negative.

- id: sarcasm_003
  - text: 这服务真棒，排队排到天荒地老。
  - context: 医院挂号体验
  - gold: negative
  - prediction: neutral
  - raw_output: >
    1.  **Analyze the Request:**
        *   Task: Determine the true emotional sentiment of a given text in context.
        *   Input: Text ("这服务真棒，排队排到天荒地老。") and Context ("医院挂号体验").
        *   Output: Exactly one label from

- id: sarcasm_004
  - text: 哇，今天又准时下班了呢，感动。
  - context: 加班抱怨
  - gold: negative
  - prediction: neutral
  - raw_output: >
    1.  **Analyze the Request:**
        *   Task: Determine the true emotional sentiment of a given text based on its context.
        *   Input: Text ("哇，今天又准时下班了呢，感动。") and Context ("加班抱怨" - complaining about overtime).
        *   Output: Exactly

- id: sarcasm_005
  - text: Great, the app crashed right before submit.
  - context: 提交表单时程序崩溃
  - gold: negative
  - prediction: neutral
  - raw_output: >
    1.  **Analyze the Request:**
        *   Task: Determine the true emotional sentiment of the given text, considering the context.
        *   Input Text: "Great, the app crashed right before submit."
        *   Input Context: "提交表单时程序崩溃" (The app crashed when

### 类型：adversarial

- id: adv_001
  - text: 谢谢你哈🙂，方案写得真‘周到’。
  - context: 引号反语 + emoji
  - gold: negative
  - prediction: neutral
  - raw_output: >
    1.  **Analyze the Request:**
        *   Task: Determine the true emotional sentiment of the given text based on the text and context.
        *   Input Text: "谢谢你哈🙂，方案写得真‘周到’。" (Thank you 🙂, the proposal is written so 'thoughtfully'.)

- id: adv_002
  - text: 这波操作太6了吧，文档直接删光。
  - context: 网络语言 + 负面行为
  - gold: negative
  - prediction: neutral
  - raw_output: >
    1.  **Analyze the Request:**
        *   Task: Determine the true emotional sentiment of a given text combined with its context.
        *   Input Text: "这波操作太6了吧，文档直接删光。" (This operation is too 6, right? Deleted all the documents directly.)

- id: adv_003
  - text: Great, the update broke everything again.
  - context: 英文反讽
  - gold: negative
  - prediction: neutral
  - raw_output: >
    1.  **Analyze the Request:**
        *   Task: Determine the true emotional sentiment of the given text, considering the context.
        *   Input Text: "Great, the update broke everything again."
        *   Context: "英文反讽" (English sarcasm/irony).
        *

- id: adv_004
  - text: 你居然还记得交作业，真令人意外。
  - context: 表面肯定，真实贬义
  - gold: negative
  - prediction: neutral
  - raw_output: >
    1.  **Analyze the Request:**
        *   Task: Determine the true emotional sentiment of the given text based on the text and context.
        *   Input Text: "你居然还记得交作业，真令人意外。" (You actually remembered to hand in the homework, what a surprise.)
        *

- id: adv_005
  - text: 今天心情像掉进了冰箱。
  - context: 隐喻负面情绪
  - gold: negative
  - prediction: neutral
  - raw_output: >
    1.  **Analyze the Request:**
        *   Task: Determine the true emotional sentiment of the given text combined with its context.
        *   Input Text: "今天心情像掉进了冰箱。" (Today my mood is like falling into a refrigerator.)
        *   Input Context: "隐喻负面情绪

## 模型：minimax-m2.5

### 类型：normal

- id: normal_001
  - text: 今天拿到奖学金，我真的很开心。
  - context: 学生收到好消息
  - gold: positive
  - prediction: neutral
  - raw_output: >
    

- id: normal_002
  - text: 这次演讲被大家认可，我心里很满足。
  - context: 公开表达获得认可
  - gold: positive
  - prediction: neutral
  - raw_output: >
    

- id: normal_003
  - text: 收到录用通知后，我整个人都轻松了。
  - context: 求职成功
  - gold: positive
  - prediction: neutral
  - raw_output: >
    

- id: normal_004
  - text: 同事帮我解决了难题，我特别感谢。
  - context: 团队协作顺利
  - gold: positive
  - prediction: neutral
  - raw_output: >
    

- id: normal_005
  - text: 新项目推进顺利，让我很有干劲。
  - context: 工作进展好
  - gold: positive
  - prediction: neutral
  - raw_output: >
    

### 类型：metaphor

- id: metaphor_001
  - text: 她的笑容像春天的阳光。
  - context: 温暖感受
  - gold: positive
  - prediction: neutral
  - raw_output: >
    

- id: metaphor_002
  - text: 那句鼓励像一盏灯，照亮了我的路。
  - context: 被鼓励
  - gold: positive
  - prediction: neutral
  - raw_output: >
    

- id: metaphor_003
  - text: 他的支持像一阵顺风，把我推向前方。
  - context: 支持带来帮助
  - gold: positive
  - prediction: neutral
  - raw_output: >
    

- id: metaphor_004
  - text: 这个想法像打开了一扇窗。
  - context: 灵感涌现
  - gold: positive
  - prediction: neutral
  - raw_output: >
    

- id: metaphor_005
  - text: 老师的点评像一把钥匙，帮我找到了答案。
  - context: 学习突破
  - gold: positive
  - prediction: neutral
  - raw_output: >
    

### 类型：sarcasm

- id: sarcasm_001
  - text: 谢谢你哈🙂，让我等了两个小时。
  - context: 用户在吐槽客服迟到
  - gold: negative
  - prediction: neutral
  - raw_output: >
    

- id: sarcasm_002
  - text: 你可真会照顾人。
  - context: 朋友忘了帮忙
  - gold: negative
  - prediction: neutral
  - raw_output: >
    

- id: sarcasm_003
  - text: 这服务真棒，排队排到天荒地老。
  - context: 医院挂号体验
  - gold: negative
  - prediction: neutral
  - raw_output: >
    

- id: sarcasm_004
  - text: 哇，今天又准时下班了呢，感动。
  - context: 加班抱怨
  - gold: negative
  - prediction: neutral
  - raw_output: >
    

- id: sarcasm_005
  - text: Great, the app crashed right before submit.
  - context: 提交表单时程序崩溃
  - gold: negative
  - prediction: neutral
  - raw_output: >
    

### 类型：adversarial

- id: adv_001
  - text: 谢谢你哈🙂，方案写得真‘周到’。
  - context: 引号反语 + emoji
  - gold: negative
  - prediction: neutral
  - raw_output: >
    

- id: adv_002
  - text: 这波操作太6了吧，文档直接删光。
  - context: 网络语言 + 负面行为
  - gold: negative
  - prediction: neutral
  - raw_output: >
    

- id: adv_003
  - text: Great, the update broke everything again.
  - context: 英文反讽
  - gold: negative
  - prediction: neutral
  - raw_output: >
    

- id: adv_004
  - text: 你居然还记得交作业，真令人意外。
  - context: 表面肯定，真实贬义
  - gold: negative
  - prediction: neutral
  - raw_output: >
    

- id: adv_005
  - text: 今天心情像掉进了冰箱。
  - context: 隐喻负面情绪
  - gold: negative
  - prediction: neutral
  - raw_output: >
    

## 模型：gemini-2.5-baseline

### 类型：normal

- id: normal_001
  - text: 今天拿到奖学金，我真的很开心。
  - context: 学生收到好消息
  - gold: positive
  - prediction: neutral
  - raw_output: >
    

- id: normal_002
  - text: 这次演讲被大家认可，我心里很满足。
  - context: 公开表达获得认可
  - gold: positive
  - prediction: neutral
  - raw_output: >
    label

- id: normal_003
  - text: 收到录用通知后，我整个人都轻松了。
  - context: 求职成功
  - gold: positive
  - prediction: neutral
  - raw_output: >
    

- id: normal_004
  - text: 同事帮我解决了难题，我特别感谢。
  - context: 团队协作顺利
  - gold: positive
  - prediction: neutral
  - raw_output: >
    

- id: normal_005
  - text: 新项目推进顺利，让我很有干劲。
  - context: 工作进展好
  - gold: positive
  - prediction: neutral
  - raw_output: >
    

### 类型：metaphor

- id: metaphor_001
  - text: 她的笑容像春天的阳光。
  - context: 温暖感受
  - gold: positive
  - prediction: neutral
  - raw_output: >
    

- id: metaphor_002
  - text: 那句鼓励像一盏灯，照亮了我的路。
  - context: 被鼓励
  - gold: positive
  - prediction: neutral
  - raw_output: >
    

- id: metaphor_003
  - text: 他的支持像一阵顺风，把我推向前方。
  - context: 支持带来帮助
  - gold: positive
  - prediction: neutral
  - raw_output: >
    

- id: metaphor_004
  - text: 这个想法像打开了一扇窗。
  - context: 灵感涌现
  - gold: positive
  - prediction: neutral
  - raw_output: >
    

- id: metaphor_005
  - text: 老师的点评像一把钥匙，帮我找到了答案。
  - context: 学习突破
  - gold: positive
  - prediction: neutral
  - raw_output: >
    

### 类型：sarcasm

- id: sarcasm_001
  - text: 谢谢你哈🙂，让我等了两个小时。
  - context: 用户在吐槽客服迟到
  - gold: negative
  - prediction: neutral
  - raw_output: >
    

- id: sarcasm_002
  - text: 你可真会照顾人。
  - context: 朋友忘了帮忙
  - gold: negative
  - prediction: neutral
  - raw_output: >
    

- id: sarcasm_003
  - text: 这服务真棒，排队排到天荒地老。
  - context: 医院挂号体验
  - gold: negative
  - prediction: neutral
  - raw_output: >
    

- id: sarcasm_004
  - text: 哇，今天又准时下班了呢，感动。
  - context: 加班抱怨
  - gold: negative
  - prediction: neutral
  - raw_output: >
    label

- id: sarcasm_006
  - text: 真是个完美的安排，雨天停电。
  - context: 天气与停电同时发生
  - gold: negative
  - prediction: neutral
  - raw_output: >
    

### 类型：adversarial

- id: adv_001
  - text: 谢谢你哈🙂，方案写得真‘周到’。
  - context: 引号反语 + emoji
  - gold: negative
  - prediction: neutral
  - raw_output: >
    

- id: adv_002
  - text: 这波操作太6了吧，文档直接删光。
  - context: 网络语言 + 负面行为
  - gold: negative
  - prediction: neutral
  - raw_output: >
    label

- id: adv_003
  - text: Great, the update broke everything again.
  - context: 英文反讽
  - gold: negative
  - prediction: neutral
  - raw_output: >
    label

- id: adv_004
  - text: 你居然还记得交作业，真令人意外。
  - context: 表面肯定，真实贬义
  - gold: negative
  - prediction: neutral
  - raw_output: >
    

- id: adv_005
  - text: 今天心情像掉进了冰箱。
  - context: 隐喻负面情绪
  - gold: negative
  - prediction: neutral
  - raw_output: >
    

## 模型：qwen3.5-plus

### 类型：normal

- id: normal_002
  - text: 这次演讲被大家认可，我心里很满足。
  - context: 公开表达获得认可
  - gold: positive
  - prediction: neutral
  - raw_output: >
    

- id: normal_003
  - text: 收到录用通知后，我整个人都轻松了。
  - context: 求职成功
  - gold: positive
  - prediction: neutral
  - raw_output: >
    

- id: normal_004
  - text: 同事帮我解决了难题，我特别感谢。
  - context: 团队协作顺利
  - gold: positive
  - prediction: neutral
  - raw_output: >
    

- id: normal_005
  - text: 新项目推进顺利，让我很有干劲。
  - context: 工作进展好
  - gold: positive
  - prediction: neutral
  - raw_output: >
    

- id: normal_006
  - text: 家人送来的消息让我很温暖。
  - context: 家庭支持
  - gold: positive
  - prediction: neutral
  - raw_output: >
    

### 类型：metaphor

- id: metaphor_001
  - text: 她的笑容像春天的阳光。
  - context: 温暖感受
  - gold: positive
  - prediction: neutral
  - raw_output: >
    

- id: metaphor_002
  - text: 那句鼓励像一盏灯，照亮了我的路。
  - context: 被鼓励
  - gold: positive
  - prediction: neutral
  - raw_output: >
    

- id: metaphor_003
  - text: 他的支持像一阵顺风，把我推向前方。
  - context: 支持带来帮助
  - gold: positive
  - prediction: neutral
  - raw_output: >
    

- id: metaphor_004
  - text: 这个想法像打开了一扇窗。
  - context: 灵感涌现
  - gold: positive
  - prediction: neutral
  - raw_output: >
    

- id: metaphor_005
  - text: 老师的点评像一把钥匙，帮我找到了答案。
  - context: 学习突破
  - gold: positive
  - prediction: neutral
  - raw_output: >
    

### 类型：sarcasm

- id: sarcasm_001
  - text: 谢谢你哈🙂，让我等了两个小时。
  - context: 用户在吐槽客服迟到
  - gold: negative
  - prediction: neutral
  - raw_output: >
    

- id: sarcasm_002
  - text: 你可真会照顾人。
  - context: 朋友忘了帮忙
  - gold: negative
  - prediction: neutral
  - raw_output: >
    

- id: sarcasm_003
  - text: 这服务真棒，排队排到天荒地老。
  - context: 医院挂号体验
  - gold: negative
  - prediction: neutral
  - raw_output: >
    

- id: sarcasm_004
  - text: 哇，今天又准时下班了呢，感动。
  - context: 加班抱怨
  - gold: negative
  - prediction: neutral
  - raw_output: >
    

- id: sarcasm_005
  - text: Great, the app crashed right before submit.
  - context: 提交表单时程序崩溃
  - gold: negative
  - prediction: neutral
  - raw_output: >
    

### 类型：adversarial

- id: adv_001
  - text: 谢谢你哈🙂，方案写得真‘周到’。
  - context: 引号反语 + emoji
  - gold: negative
  - prediction: neutral
  - raw_output: >
    

- id: adv_002
  - text: 这波操作太6了吧，文档直接删光。
  - context: 网络语言 + 负面行为
  - gold: negative
  - prediction: neutral
  - raw_output: >
    

- id: adv_003
  - text: Great, the update broke everything again.
  - context: 英文反讽
  - gold: negative
  - prediction: neutral
  - raw_output: >
    

- id: adv_004
  - text: 你居然还记得交作业，真令人意外。
  - context: 表面肯定，真实贬义
  - gold: negative
  - prediction: neutral
  - raw_output: >
    

- id: adv_005
  - text: 今天心情像掉进了冰箱。
  - context: 隐喻负面情绪
  - gold: negative
  - prediction: neutral
  - raw_output: >
    
