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
    
