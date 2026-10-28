# 哈密顿块（hw8 Q5–Q8）的讲法与已核结果

## 交付节奏

- 他按题追进度：「下一题呢」＝直接进下一题，不要复述上一题结论、不要报总进度。每题一屏半以内，公式逐行演算，末句给一条可自查的判据。
- 每题收尾一句「这节已落 wiki、校验全绿、已推送」即可，他不看仓库细节。
- 题目里出现「特别关注 X」时，X 就是唯一考点：先把 X 算出来并解释它的符号与含义，其余按流程走。

## Q5 相空间变分

三个必讲点：

1. 变分对象从一条曲线变成一对独立曲线 ⇒ 端点固定**四个**量（$\delta q$、$\delta p$ 各两端）。少固定一个，边界项就消不掉——这是题目把四个零条件都写出来的原因。
2. 作用量为什么是 $-q_\alpha\dot p_\alpha-H$：与 $p\dot q-H$ 只差全导数 $d(pq)/dt$，对固定端点的变分无影响；选它的理由是导数只落在 $p$ 上，一次分部积分同时得到两条对称的一阶方程。
3. 计算只有一项要分部积分：$-\int q_\alpha\,\delta\dot p_\alpha=-[q_\alpha\delta p_\alpha]+\int\dot q_\alpha\,\delta p_\alpha$，边界项靠 $\delta p=0$ 消掉，剩下 $(\dot q-\partial H/\partial p)\delta p$ 与 $-(\dot p+\partial H/\partial q)\delta q$，两者独立故各为零。

概念点：第二条才是运动方程，第一条是 $p=\partial L/\partial\dot q$ 的反解（定义），不要并列成「两条新物理」。

## Q6 把时间降格为坐标

- 速度变成比 $v_\alpha=\dot q_\alpha/\dot q_0$；$p_\alpha$ 不变（$1/\dot q_0$ 与 $\dot q_0$ 因子相消），顺带说明动量不依赖参数化。
- $p_0=\partial L_1/\partial\dot q_0=L-\sum p_\alpha v_\alpha=-H$。**负号是最常漏的一处**，讲法是「定义与哈密顿量的定义并排放」。
- $H_1=\sum p_\beta\dot q_\beta-L_1\equiv0$：$\sum p_\alpha v_\alpha-L$ 正是 $H$，两项抵消。
- **必须主动点出勒让德变换在这里退化**：$p_0$ 不含 $\dot q_0$ ⇒ $\dot q_0$ 解不出来 ⇒ 多出的动量不独立，被约束 $p_0+H=0$ 卡住。不点这一层，他一定会问「$H_1$ 恒为零，怎么还能求导出方程」。
- 正则方程把 $H_1$ 写成 $\dot q_0(p_0+H)$：$\alpha$ 方向约掉 $\dot q_0$ 回到原方程；$t$ 方向两条 $\dot q_0=\partial H_1/\partial p_0$、$\dot p_0=-\partial H_1/\partial q_0$ 都是恒等式，分别翻译成 $dp_0/dt=-\partial H/\partial t$ 与 $dH/dt=\partial H/\partial t$。
- 守恒常数是 **0**；真正有内容的是 $p_0=-E$（$H$ 不显含 $t$ 时的诺特荷）。

## Q7 全导数的相空间版本

- $p'_\alpha=p_\alpha+\partial f/\partial q_\alpha$；$H'=H-\partial f/\partial t$。$H'$ 里用的是旧 $p$，必须代回 $p=p'-\partial f/\partial q$ 才是 $(q,p')$ 的函数，漏掉这步后面必错。
- 等价性：$\dot q$ 方程白给；$\dot p$ 方程的难点是**对 $q$ 求导时固定 $p'$ 而不是 $p$**，会多出 $-\sum_\beta(\partial H/\partial p_\beta)\,\partial^2f/\partial q_\alpha\partial q_\beta$，它与 $d(\partial f/\partial q_\alpha)/dt$ 里的求和项相消。
- 旁注一句：这就是正则变换，$f$ 是生成函数，「正则」＝不改变方程形式。不作主线。

## Q8 球面摆

- 约定 $\theta$ 自竖直向下量，$V=-mgl\cos\theta$；$H=\frac{p_\theta^2}{2ml^2}+\frac{p_\varphi^2}{2ml^2\sin^2\theta}-mgl\cos\theta$，$\sin^2\theta$ 来自 $\varphi$ 方向的度量系数 $l\sin\theta$。
- 正则方程四条；消动量得 $\ddot\theta=\sin\theta\cos\theta\,\dot\varphi^2-\frac gl\sin\theta$，配 $\frac{d}{dt}(\sin^2\theta\,\dot\varphi)=0$。
- 守恒量：$E$ 与 $p_\varphi=ml^2\sin^2\theta\,\dot\varphi$，两者独立且对合 ⇒ 刘维尔可积；$\theta$ 走一维有效势 $U_{\rm eff}=\frac{p_\varphi^2}{2ml^2\sin^2\theta}-mgl\cos\theta$（$p_\varphi\ne0$ 时唯一极小落在 $(0,\pi/2)$）。圆锥运动条件 $\cos\theta\,\dot\varphi^2=g/l$。
- **陷阱（他会记错）：总角动量不守恒**，$|\mathbf L|^2$ 也不守恒，只有 $L_z$；重力对球心有力矩，中心力场的直觉不能搬过来。
- 小振动退化：$\theta$ 与 $\varphi$ 频率同为 $\sqrt{g/l}$，轨道闭合如各向同性二维振子——频率偶然相等，不是新积分。

## 已落页

`转动惯量张量与惯量主轴`、`欧拉陀螺`、`相空间变分与正则方程`、`球面摆`；`全导数不改变动力学` 补了「相空间里的版本」一节。`_索引.md` 分「刚体」「哈密顿力学」两组。
