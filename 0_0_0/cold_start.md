[1]
首先我觉得我们应该有一个全局的启动，还有各个任务的启动，这是分开的。
这里具体需要考虑的就是启动的时候，我们以什么样的形式去收集信息，其实这里无非就两种形式：
1）预生成的问卷填写
2）和模型的对话
我们可以结合两种形式，首先用户需且填写一些信息，然后在之后会和模型进行多轮的对话（当智能体判断信息足够的时候就会喊停），结合两者来提供全面的信息。
