<template>
    <div style="height: 100%; width: 100%" ref="myref"></div>
</template>


<script>
    import mermaid from 'mermaid';
    import {
        Tabbar,
        Form,
        Layout,
        Chart,
        Grid,
        DataCollection,
    } from "dhx-suite";

    export default {
        name: "app",
        data: () => ({
            maintabbar: null,
            form1: null,
            form2: null,
            form3: null,
            form4: null,
            resform: null,
            infoform: null,
            reslayout: null,
            vposlayout: null,
            restabbar: null,
            chart: null,

            grid_cur: null,
            grid_pos: null,
            grid_rank: null,
            grid_srank: null,
            grid_add: null,
            grid_steam: null,
            grid_nrank: null,

            dgrid_cur: null,
            dgrid_pos: null,
            dgrid_rank: null,
            dgrid_srank: null,
            dgrid_add: null,
            dgrid_steam: null,
            dgrid_nrank: null,

            teamcnt: 0,
            double: 0,
            bo: 0,
            wscore: 0,
            lscore: 0,
            dscore: 0,
            teamnames: [],
            scoreboard: [],
            matchleftcnt: 0,
            matchleft: [],
            showtop: 0,
            showbot: 0,
            toprank: 0,
            botrank: 0,
            sadd: 0,
            srank: 0,
            snext: 0,
            steam: 0,
            steamr1: 0,
            steamr2: 0,
            nteam1: 0,
            nteam2: 0,
            mostml: 0,
        }),
        mounted() {
            this.init();
        },
        methods: {
            init() {
                $.ajaxSetup({
                    headers: {
                        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
                    }
                });
                this.teamcnt = 0;
                this.double = 1;
                this.bo = 1;
                this.wscore = 0;
                this.lscore = 0;
                this.dscore = 0;

                this.maintabbar = new Tabbar(this.$refs.myref, {
                    mode: "top",
                    css: "dhx_widget--bordered",
                    views: [
                        { tab: "指定赛制", id: "tab1" },
                        { tab: "输入队名", id: "tab2" },
                        { tab: "输入比分", id: "tab3" },
                        { tab: "指定输出形式", id: "tab4" },
                        { tab: "计算结果", id: "tab5" }
                    ],
                    disabled: ["tab2", "tab3", "tab4", "tab5"]
                });
                this.init1(false);
            },
            init1(pre) {
                const that = this;
                
                this.form1 = new Form(null, {
                    css: "dhx_widget--bordered",
                    rows: [
                        {
                            type: "input",
                            label: "参赛队伍数量",
                            name: "teamcnt",
                            inputType: "number",
                            value: this.teamcnt,
                            width: 100,
                        },
                        {
                            type: "text",
                            value: "赛制"
                        },
                        {
                            cols: [
                                {
                                    type: "select",
                                    name: "bo",
                                    width: 100,
                                    options: [
                                        {
                                            value: -1,
                                            content: "自由得分"
                                        },
                                        {
                                            value: 1,
                                            content: "一局定胜负",
                                        },
                                        {
                                            value: 3,
                                            content: "三局两胜"
                                        },
                                        {
                                            value: 5,
                                            content: "五局三胜"
                                        },
                                        {
                                            value: 7,
                                            content: "七局四胜"
                                        },
                                    ],
                                    value: this.bo
                                },
                                {
                                    type: "spacer",
                                    width: 100
                                },
                                {
                                    type: "select",
                                    name: "double",
                                    width: 100,
                                    options: [
                                        {
                                            value: 1,
                                            content: "单循环",
                                        },
                                        {
                                            value: 2,
                                            content: "双循环"
                                        },
                                    ],
                                    value: this.double
                                }
                            ]
                        },
                        {
                            type: "text",
                            value: "以下仅在自由得分赛制下可用，请输入整数"
                        },
                        {
                            type: "input",
                            label: "获胜积分",
                            labelPosition: "left",
                            name: "wscore",
                            inputType: "number",
                            value: this.wscore,
                            width: 180,
                            disabled: this.bo != -1
                        },
                        {
                            type: "input",
                            label: "平局积分",
                            labelPosition: "left",
                            name: "dscore",
                            inputType: "number",
                            value: this.dscore,
                            width: 180,
                            disabled: this.bo != -1
                        },
                        {
                            type: "input",
                            label: "战败积分",
                            labelPosition: "left",
                            name: "lscore",
                            inputType: "number",
                            value: this.lscore,
                            width: 180,
                            disabled: this.bo != -1
                        },
                        {
                            cols: [
                                {
                                    type: "button",
                                    value: "下一步",
                                    name: "next",
                                },
                                {
                                    type: "spacer",
                                    width: 50
                                },
                                {
                                    type: "button",
                                    value: "重置",
                                    name: "reset",
                                },
                                {
                                    type: "spacer",
                                    width: 50
                                },
                                {
                                    type: "button",
                                    value: "载入数据",
                                    name: "load",
                                }
                            ]
                        },
                        {
                            type: "text",
                            value: "*系统完善中，可能暂时无法涵盖所有赛制，敬请谅解。"
                        },
                        {
                            type: "text",
                            name: "preinfo"
                        }
                    ]
                });
                if (pre) {
                    this.form1.getItem("preinfo").setValue("*您已填写后续步骤的内容，修改赛制会导致这些内容失效");
                }
                this.maintabbar.getCell("tab1").attach(this.form1);
                function getmostml(x) {
                    if (x == 1) {
                        return 16;
                    }
                    else if (x == 3) {
                        return 8;
                    }
                    else if (x == 5) {
                        return 6;
                    }
                    else if (x == 7) {
                        return 5;
                    }
                    else {
                        return 10;
                    }
                }
                this.form1.getItem("bo").events.on("change", function (events) {
                    const t = that.form1.getItem("bo").getValue();
                    if (t == -1) {
                        that.form1.getItem("wscore").enable();
                        that.form1.getItem("lscore").enable();
                        that.form1.getItem("dscore").enable();
                    }
                    else {
                        that.form1.getItem("wscore").setValue(0);
                        that.form1.getItem("lscore").setValue(0);
                        that.form1.getItem("dscore").setValue(0);
                        that.form1.getItem("wscore").disable();
                        that.form1.getItem("lscore").disable();
                        that.form1.getItem("dscore").disable();
                    }
                });

                const fileInput = document.createElement("input");
                fileInput.type = "file";
                fileInput.accept = ".json";
                fileInput.style.display = "none";
                document.body.appendChild(fileInput);

                function filecheck(data) {
                    if (!("teamcnt" in data) || !("double" in data) || !("bo" in data) || !("wscore" in data) || !("lscore" in data) || !("dscore" in data)) {
                        return false
                    }
                    if (!("teamnames" in data) || !("scoreboard" in data) || !("matchleftcnt" in data) || !("matchleft" in data) || !("showtop" in data) || !("showbot" in data)) {
                        return false
                    }
                    if (!("toprank" in data) || !("botrank" in data) || !("sadd" in data) || !("srank" in data) || !("snext" in data) || !("steam" in data)) {
                        return false
                    }
                    if (!("steamr1" in data) || !("steamr2" in data) || !("nteam1" in data) || !("nteam2" in data) || !("mostml" in data)) {
                        return false
                    }
                    return true
                }

                this.form1.getItem("load").events.on("click", () => {
                    fileInput.value = "";
                    fileInput.click();
                });
                fileInput.addEventListener("change", async (e) => {
                    const file = e.target.files[0];
                    if (!file) return;

                    try {
                        const data = JSON.parse(await file.text());
                        if (!filecheck(data)) {
                            throw new Error("文件格式错误");
                        }
                        that.teamcnt = data.teamcnt;
                        that.double = data.double;
                        that.bo = data.bo;
                        that.wscore = data.wscore;
                        that.lscore = data.lscore;
                        that.dscore = data.dscore;
                        that.teamnames = data.teamnames;
                        that.scoreboard = data.scoreboard;
                        that.matchleftcnt = data.matchleftcnt;
                        that.matchleft = data.matchleft;
                        that.showtop = data.showtop;
                        that.showbot = data.showbot;
                        that.toprank = data.toprank;
                        that.botrank = data.botrank;
                        that.sadd = data.sadd;
                        that.srank = data.srank;
                        that.snext = data.snext;
                        that.steam = data.steam;
                        that.steamr1 = data.steamr1;
                        that.steamr2 = data.steamr2;
                        that.nteam1 = data.nteam1;
                        that.nteam2 = data.nteam2;
                        that.mostml = data.mostml;

                        that.maintabbar.enableTab("tab4");
                        that.maintabbar.setActive("tab4");
                        that.maintabbar.disableTab("tab1");
                        that.init4();
                    } catch (error) {
                        alert("文件读取失败：" + error.message);
                    }
                });

                this.form1.getItem("next").events.on("click", function (events) {
                    var submitflag = true;
                    var preflag = false;
                    if (that.teamcnt != that.form1.getItem("teamcnt").getValue()) {
                        that.teamcnt = that.form1.getItem("teamcnt").getValue();
                        preflag = true;
                    }
                    if (that.bo != that.form1.getItem("bo").getValue()) {
                        that.bo = that.form1.getItem("bo").getValue();
                        preflag = true;
                    }
                    if (that.double != that.form1.getItem("double").getValue()) {
                        that.double = that.form1.getItem("double").getValue();
                        preflag = true;
                    }
                    that.wscore = that.form1.getItem("wscore").getValue();
                    that.lscore = that.form1.getItem("lscore").getValue();
                    that.dscore = that.form1.getItem("dscore").getValue();
                    that.mostml = getmostml(that.bo)
                    
                    if (!(Number.isInteger(that.teamcnt) && that.teamcnt >= 2 && that.teamcnt <= 10)) {
                        that.form1.getItem("teamcnt").setProperties({
                            helpMessage: "请输入2-10之间的整数",
                        });
                        alert("请输入2-10之间的整数");
                        submitflag = false;
                    }
                    else {
                        that.form1.getItem("teamcnt").setProperties({
                            helpMessage: null,
                        });
                    }
                    if (!Number.isInteger(that.wscore)) {
                        that.form1.getItem("wscore").setProperties({
                            helpMessage: "请输入整数",
                        });
                        alert("请输入整数");
                        submitflag = false;
                    }
                    else {
                        that.form1.getItem("wscore").setProperties({
                            helpMessage: null,
                        });
                    }
                    if (!Number.isInteger(that.lscore)) {
                        that.form1.getItem("lscore").setProperties({
                            helpMessage: "请输入整数",
                        });
                        alert("请输入整数");
                        submitflag = false;
                    }
                    else {
                        that.form1.getItem("lscore").setProperties({
                            helpMessage: null,
                        });
                    }
                    if (!Number.isInteger(that.dscore)) {
                        that.form1.getItem("dscore").setProperties({
                            helpMessage: "请输入整数",
                        });
                        alert("请输入整数");
                        submitflag = false;
                    }
                    else {
                        that.form1.getItem("dscore").setProperties({
                            helpMessage: null,
                        });
                    }
                    if (submitflag) {
                        if (pre == false || preflag) {
                            that.teamnames = [];
                            that.scoreboard = [];
                            for (let i = 0; i < that.teamcnt; i++) {
                                that.teamnames[i] = String.fromCharCode(65 + i);
                            }
                            for (let i = 0; i < that.teamcnt; i++) {
                                that.scoreboard.push([]);
                                for (let j = 0; j < that.teamcnt; j++) {
                                    if (that.double == 1) {
                                        that.scoreboard[i].push([0]);
                                    }
                                    else {
                                        that.scoreboard[i].push([0, 0]);
                                    }
                                }
                            }
                            that.matchleftcnt = 0;
                            that.matchleft = [];
                            that.showtop = 0;
                            that.showbot = 0;
                            that.toprank = 1;
                            that.botrank = 1;
                            that.sadd = 0;
                            that.srank = 0;
                            that.snext = 0;
                            that.steam = 0;
                            that.steamr1 = 1;
                            that.steamr2 = 1;
                            that.nteam1 = 0;
                            that.nteam2 = 0;
                        }
                        that.maintabbar.enableTab("tab2");
                        that.maintabbar.setActive("tab2");
                        that.maintabbar.disableTab("tab1");
                        that.init2();
                    }
                });
                this.form1.getItem("reset").events.on("click", function (events) {
                    that.maintabbar.destructor();
                    that.init();
                });
            },
            init2() {
                const that = this;
                const rows = [];
                for (let i = 0; i < this.teamcnt; i++) {
                    rows.push({
                        type: "input",
                        label: `队伍${i + 1}`,
                        name: `team${i + 1}`,
                        width: 100,
                        value: this.teamnames[i]
                    })
                }
                rows.push(
                    {
                        cols: [
                            {
                                type: "button",
                                value: "下一步",
                                name: "next",
                            },
                            {
                                type: "spacer",
                                width: 50
                            },
                            {
                                type: "button",
                                value: "上一步",
                                name: "pre",
                            },
                            {
                                type: "spacer",
                                width: 50
                            },
                            {
                                type: "button",
                                value: "重置",
                                name: "reset",
                            }
                        ]
                    },
                    {
                        type: "text",
                        value: "*队名不可为空、重复或超过15个字符。"
                    }
                );
                this.form2 = new Form(null, {
                    css: "dhx_widget--bordered",
                    rows
                });
                this.maintabbar.getCell("tab2").attach(this.form2);

                this.form2.getItem("next").events.on("click", function (events) {
                    var flag = true;
                    that.teamnames = [];
                    for (let i = 0; i < that.teamcnt; i++) {
                        const name = that.form2.getItem(`team${i + 1}`).getValue();
                        if (name == "") {
                            that.form2.getItem(`team${i + 1}`).setProperties({
                                helpMessage: "队名不可为空",
                            });
                            alert("队名不可为空");
                            flag = false;
                            that.form2.setFocus(`team${i + 1}`);
                        }
                        else if (name.length > 15) {
                            that.form2.getItem(`team${i + 1}`).setProperties({
                                helpMessage: "队名不可超过15个字符",
                            });
                            alert("队名不可超过15个字符");
                            flag = false;
                            that.form2.setFocus(`team${i + 1}`);
                        }
                        else if (that.teamnames.includes(name)) {
                            that.form2.getItem(`team${i + 1}`).setProperties({
                                helpMessage: "队名不可重复",
                            });
                            alert("队名不可重复");
                            flag = false;
                            that.form2.setFocus(`team${i + 1}`);
                        }
                        else {
                            that.teamnames[i] = name;
                            that.form2.getItem(`team${i + 1}`).setProperties({
                                helpMessage: null,
                            });
                        }
                    }
                    if (flag) {
                        that.maintabbar.enableTab("tab3");
                        that.maintabbar.setActive("tab3");
                        that.maintabbar.disableTab("tab2");
                        that.init3();
                    }
                });
                this.form2.getItem("pre").events.on("click", function (events) {
                    that.maintabbar.enableTab("tab1");
                    that.maintabbar.setActive("tab1");
                    that.maintabbar.disableTab("tab2");
                    that.init1(true);
                });
                this.form2.getItem("reset").events.on("click", function (events) {
                    that.maintabbar.destructor();
                    that.init();
                });
            },
            init3() {
                const that = this;
                
                const rows = [];
                if (this.bo != -1) {
                    const options = [];
                    for (let i = 0; i <= (this.bo + 1) / 2; i++) {
                        options.push({
                            value: i,
                            content: String(i)
                        });
                    }
                    var match = 1;
                    for (let i = 0; i < this.teamcnt; i++) {
                        for (let j = i + 1; j < this.teamcnt; j++) {
                            const cols = [];
                            for (let k = 0; k < that.double; k++) {
                                cols.push(
                                    {
                                        type: "select",
                                        name: `m${match}r${k}t1`,
                                        width: 50,
                                        value: this.scoreboard[i][j][k],
                                        options
                                    },
                                    {
                                        type: "spacer",
                                        width: 20
                                    },
                                    {
                                        type: "text",
                                        value: ":",
                                        width: 20,
                                    },
                                    {
                                        type: "select",
                                        name: `m${match}r${k}t2`,
                                        width: 50,
                                        value: this.scoreboard[j][i][k],
                                        options
                                    },
                                    {
                                        type: "spacer",
                                        width: 20
                                    },
                                    {
                                        type: "checkbox",
                                        name: `m${match}r${k}`,
                                        text: "该场比赛未进行",
                                        checked: this.matchleft.some(sub => sub[0] === i && sub[1] === j && sub[2] === k)
                                    }
                                )
                            }
                            rows.push(
                                {
                                    type: "text",
                                    name: `errm${match}`,
                                    labelPosition: "left",
                                    value: this.teamnames[i] + " VS " + this.teamnames[j]
                                },
                                {
                                    cols: cols
                                },
                            );
                            match++;
                        }
                    }
                }
                else {
                    var match = 1;
                    for (let i = 0; i < this.teamcnt; i++) {
                        for (let j = i + 1; j < this.teamcnt; j++) {
                            const cols = [];
                            for (let k = 0; k < that.double; k++) {
                                cols.push(
                                    {
                                        type: "input",
                                        name: `m${match}r${k}t1`,
                                        width: 100,
                                        inputType: "number",
                                        value: this.scoreboard[i][j][k],
                                    },
                                    {
                                        type: "spacer",
                                        width: 20
                                    },
                                    {
                                        type: "text",
                                        value: ":",
                                        width: 20,
                                    },
                                    {
                                        type: "input",
                                        name: `m${match}r${k}t2`,
                                        width: 100,
                                        inputType: "number",
                                        value: this.scoreboard[j][i][k],
                                    },
                                    {
                                        type: "spacer",
                                        width: 20
                                    },
                                    {
                                        type: "checkbox",
                                        name: `m${match}r${k}`,
                                        text: "该场比赛未进行",
                                        checked: this.matchleft.some(sub => sub[0] === i && sub[1] === j && sub[2] === k)
                                    }
                                )
                            }
                            rows.push(
                                {
                                    type: "text",
                                    name: `errm${match}`,
                                    labelPosition: "left",
                                    value: this.teamnames[i] + " VS " + this.teamnames[j]
                                },
                                {
                                    cols: cols
                                },
                            );
                            match++;
                        }
                    }
                }
                rows.push(
                    {
                        cols: [
                            {
                                type: "button",
                                value: "下一步",
                                name: "next",
                            },
                            {
                                type: "spacer",
                                width: 50
                            },
                            {
                                type: "button",
                                value: "上一步",
                                name: "pre",
                            },
                            {
                                type: "spacer",
                                width: 50
                            },
                            {
                                type: "button",
                                value: "重置",
                                name: "reset",
                            }
                        ]
                    }
                )
                if (this.bo != -1) {
                    rows.push(
                        {
                            type: "text",
                            value: "*每场已进行的比赛必须有且只有一方达到获胜分数。"
                        }
                    )
                }
                else {
                    rows.push(
                        {
                            type: "text",
                            value: "*每场已进行的比赛双方得分必须都是不小于0的整数。"
                        }
                    )
                }
                this.form3 = new Form(null, {
                    css: "dhx_widget--bordered",
                    rows
                });
                this.maintabbar.getCell("tab3").attach(this.form3);

                function isvalid(t1, t2) {
                    if (that.bo == -1) {
                        return Number.isInteger(t1) && Number.isInteger(t2) && t1 >= 0 && t2 >= 0;
                    }
                    else {
                        return (t1 == (that.bo + 1) / 2 && t2 < (that.bo + 1) / 2) || (t2 == (that.bo + 1) / 2 && t1 < (that.bo + 1) / 2)
                    }
                }
                this.form3.getItem("next").events.on("click", function (events) {
                    that.matchleftcnt = 0;
                    that.matchleft = [];
                    var flag = true;
                    var match = 1;
                    for (let i = 0; i < that.teamcnt; i++) {
                        for (let j = i + 1; j < that.teamcnt; j++) {
                            for (let k = 0; k < that.double; k++) {
                                const t1 = that.form3.getItem(`m${match}r${k}t1`).getValue();
                                const t2 = that.form3.getItem(`m${match}r${k}t2`).getValue();
                                const f = that.form3.getItem(`m${match}r${k}`).isChecked();
                                if (f) {
                                    that.scoreboard[i][j][k] = 0;
                                    that.scoreboard[j][i][k] = 0;
                                    that.matchleftcnt++;
                                    that.matchleft.push([i, j, k]);
                                    that.form3.getItem(`errm${match}`).setProperties({
                                        helpMessage: null,
                                    });
                                }
                                else if (isvalid(t1, t2)) {
                                    that.scoreboard[i][j][k] = t1;
                                    that.scoreboard[j][i][k] = t2;
                                    that.form3.getItem(`errm${match}`).setProperties({
                                        helpMessage: null,
                                    });
                                }
                                else {
                                    that.form3.getItem(`errm${match}`).setProperties({
                                        helpMessage: "输入有误",
                                    });
                                    alert("输入有误");
                                    flag = false;
                                    that.form3.setFocus(`errm${match}`);
                                }
                            }
                            match++;
                        }
                    }
                    if (flag) {
                        that.maintabbar.enableTab("tab4");
                        that.maintabbar.setActive("tab4");
                        that.maintabbar.disableTab("tab3");
                        that.init4();
                    }
                });
                this.form3.getItem("pre").events.on("click", function (events) {
                    that.maintabbar.enableTab("tab2");
                    that.maintabbar.setActive("tab2");
                    that.maintabbar.disableTab("tab3");
                    that.init2();
                });
                this.form3.getItem("reset").events.on("click", function (events) {
                    that.maintabbar.destructor();
                    that.init();
                });
            },
            init4() {
                const that = this;
                const optionsteam = [];
                const optionsrank = [];
                const optionstleft = [];
                for (let i = 0; i < this.teamcnt; i++) {
                    optionsteam.push({
                        value: i,
                        content: this.teamnames[i]
                    });
                    optionsrank.push({
                        value: i + 1,
                        content: String(i + 1)
                    });
                }
                for (let i = 0; i < this.matchleftcnt; i++) {
                    var str = this.teamnames[this.matchleft[i][0]] + " VS " + this.teamnames[this.matchleft[i][1]];
                    if (this.double == 2) {
                        optionstleft.push(
                            {
                                value: i,
                                content: str + " 第" + String(this.matchleft[i][2] + 1) + "场"
                            }
                        );
                    }
                    else {
                        optionstleft.push(
                            {
                                value: i,
                                content: str
                            }
                        );
                    }
                }
                if (this.matchleftcnt == 0) {
                    optionstleft.push(
                        {
                            value: 0,
                            content: null
                        }
                    );
                }
                this.form4 = new Form(null, {
                    css: "dhx_widget--bordered",
                    rows: [
                        {
                            cols: [
                                {
                                    type: "checkbox",
                                    name: "showtop",
                                    text: "显示排名前列的概率",
                                    width: 200,
                                    checked: this.showtop == 1
                                },
                                {
                                    type: "spacer",
                                    width: 50
                                },
                                {
                                    type: "select",
                                    name: "toprank",
                                    label: "第一名到第",
                                    labelPosition: "left",
                                    width: 150,
                                    options: optionsrank,
                                    value: this.toprank,
                                    disabled: this.showtop == 0
                                },
                                {
                                    type: "spacer",
                                    width: 10
                                },
                                {
                                    type: "text",
                                    value: "名为前列"
                                },
                                
                            ]
                        },
                        {
                            cols: [
                                {
                                    type: "checkbox",
                                    name: "showbot",
                                    text: "显示排名末尾的概率",
                                    width: 200,
                                    checked: this.showbot == 1
                                },
                                {
                                    type: "spacer",
                                    width: 50
                                },
                                {
                                    type: "select",
                                    name: "botrank",
                                    label: "第",
                                    labelPosition: "left",
                                    width: 100,
                                    options: optionsrank,
                                    value: this.botrank,
                                    disabled: this.showbot == 0
                                },
                                {
                                    type: "spacer",
                                    width: 10
                                },
                                {
                                    type: "text",
                                    value: "名到最后一名为末尾"
                                },
                            ]
                        },
                        {
                            type: "checkbox",
                            name: "sadd",
                            text: this.bo == -1 ? "显示同分筛选" : "显示加赛筛选",
                            checked: this.sadd == 1
                        },
                        {
                            type: "checkbox",
                            name: "srank",
                            text: "显示排名筛选",
                            checked: this.srank == 1
                        },
                        {
                            cols: [
                                {
                                    type: "select",
                                    name: "steam",
                                    label: "队伍名称",
                                    width: 100,
                                    options: optionsteam,
                                    value: this.steam,
                                    disabled: this.srank == 0
                                },
                                {
                                    type: "spacer",
                                    width: 50
                                },
                                {
                                    type: "select",
                                    name: "steamr1",
                                    label: "筛选起始排名",
                                    width: 100,
                                    options: optionsrank,
                                    value: this.steamr1,
                                    disabled: this.srank == 0
                                },
                                {
                                    type: "spacer",
                                    width: 50
                                },
                                {
                                    type: "select",
                                    name: "steamr2",
                                    label: "筛选终止排名",
                                    width: 100,
                                    options: optionsrank,
                                    value: this.steamr2,
                                    disabled: this.srank == 0
                                },
                            ]
                        },
                        {
                            type: "checkbox",
                            name: "snext",
                            text: "显示下场分类概率",
                            width: 200,
                            checked: this.snext == 1
                        },
                        {
                            type: "select",
                            name: "nteam",
                            label: "分类概率对战双方",
                            labelPosition: "left",
                            width: 280,
                            options: optionstleft,
                            value: 0,
                            disabled: this.snext == 0
                        },
                        {
                            type: "text",
                            name: "errm2",
                            labelPosition: "left",
                            value: "剩余比赛场次顺序"
                        },
                        {
                            type: "select",
                            name: "mlseq1",
                            label: "第一场",
                            labelPosition: "left",
                            width: 200,
                            options: optionstleft,
                            value: 0,
                            disabled: true
                        },
                        {
                            type: "select",
                            name: "mlseq2",
                            label: "第二场",
                            labelPosition: "left",
                            width: 200,
                            options: optionstleft,
                            value: 1,
                            disabled: true
                        },
                        {
                            type: "select",
                            name: "mlseq3",
                            label: "第三场",
                            labelPosition: "left",
                            width: 200,
                            options: optionstleft,
                            value: 2,
                            disabled: true
                        },
                        {
                            cols: [
                                {
                                    type: "button",
                                    value: "下一步",
                                    name: "next",
                                    loading: false
                                },
                                {
                                    type: "spacer",
                                    width: 50
                                },
                                {
                                    type: "button",
                                    value: "上一步",
                                    name: "pre",
                                },
                                {
                                    type: "spacer",
                                    width: 50
                                },
                                {
                                    type: "button",
                                    value: "重置",
                                    name: "reset",
                                }
                            ]
                        },
                        {
                            type: "text",
                            name: "errm3",
                        }
                    ]
                });
                this.maintabbar.getCell("tab4").attach(this.form4);
                
                this.form4.getItem("next").enable();
                this.form4.getItem("pre").enable();
                this.form4.getItem("reset").enable();
                if (this.matchleftcnt > this.mostml) {
                    this.form4.getItem("sadd").disable();
                    this.form4.getItem("sadd").setValue(false);
                    this.form4.getItem("srank").disable();
                    this.form4.getItem("srank").setValue(false);
                    this.form4.getItem("snext").disable();
                    this.form4.getItem("snext").setValue(false);
                    this.form4.getItem("steam").disable();
                    this.form4.getItem("steamr1").disable();
                    this.form4.getItem("steamr2").disable();
                    this.form4.getItem("nteam").disable();
                    this.form4.getItem("errm3").setProperties({
                        label: "*剩余比赛过多，排名概率将采用蒙特卡洛模拟计算，其他输出筛选将禁用。",
                    });
                }
                else if (this.matchleftcnt > 3) {
                    this.form4.getItem("errm2").setProperties({
                        helpMessage: "剩余比赛超过3场，以下内容无需填写。",
                    });
                }
                else if (this.matchleftcnt == 0) {
                    this.form4.getItem("showtop").disable();
                    this.form4.getItem("showtop").setValue(false);
                    this.form4.getItem("showbot").disable();
                    this.form4.getItem("showbot").setValue(false);
                    this.form4.getItem("sadd").disable();
                    this.form4.getItem("sadd").setValue(false);
                    this.form4.getItem("srank").disable();
                    this.form4.getItem("srank").setValue(false);
                    this.form4.getItem("snext").disable();
                    this.form4.getItem("snext").setValue(false);
                    this.form4.getItem("toprank").disable();
                    this.form4.getItem("botrank").disable();
                    this.form4.getItem("steam").disable();
                    this.form4.getItem("steamr1").disable();
                    this.form4.getItem("steamr2").disable();
                    this.form4.getItem("nteam").disable();
                    this.form4.getItem("errm3").setProperties({
                        label: "*所有比赛已结束，无需计算概率，请直接点击提交。",
                    });
                }
                if (this.matchleftcnt == 3) {
                    this.form4.getItem("mlseq3").enable();
                }
                if (this.matchleftcnt == 2 || this.matchleftcnt == 3) {
                    this.form4.getItem("mlseq2").enable();
                }
                if (this.matchleftcnt == 1 || this.matchleftcnt == 2 || this.matchleftcnt == 3) {
                    this.form4.getItem("mlseq1").enable();
                }
                this.form4.getItem("showtop").events.on("change", function (events) {
                    const f = that.form4.getItem("showtop").isChecked();
                    if (f) {
                        that.form4.getItem("toprank").enable();
                    }
                    else {
                        that.form4.getItem("toprank").disable();
                    }
                })
                this.form4.getItem("showbot").events.on("change", function (events) {
                    const f = that.form4.getItem("showbot").isChecked();
                    if (f) {
                        that.form4.getItem("botrank").enable();
                    }
                    else {
                        that.form4.getItem("botrank").disable();
                    }
                })
                this.form4.getItem("srank").events.on("change", function (events) {
                    const f = that.form4.getItem("srank").isChecked();
                    if (f) {
                        that.form4.getItem("steam").enable();
                        that.form4.getItem("steamr1").enable();
                        that.form4.getItem("steamr2").enable();
                    }
                    else {
                        that.form4.getItem("steam").disable();
                        that.form4.getItem("steamr1").disable();
                        that.form4.getItem("steamr2").disable();
                    }
                })
                this.form4.getItem("snext").events.on("change", function (events) {
                    const f = that.form4.getItem("snext").isChecked();
                    if (f) {
                        that.form4.getItem("nteam").enable();
                    }
                    else {
                        that.form4.getItem("nteam").disable();
                    }
                })

                this.form4.getItem("next").events.on("click", function (events) {
                    that.form4.getItem("steam").setProperties({
                        helpMessage: null,
                    });
                    var submitflag = true;

                    that.showtop = that.form4.getItem("showtop").isChecked() ? 1 : 0;
                    that.showbot = that.form4.getItem("showbot").isChecked() ? 1 : 0;
                    that.sadd = that.form4.getItem("sadd").isChecked() ? 1 : 0;
                    that.srank = that.form4.getItem("srank").isChecked() ? 1 : 0;
                    that.snext = that.form4.getItem("snext").isChecked() ? 1 : 0;
                    if (that.showtop) {
                        that.toprank = that.form4.getItem("toprank").getValue();
                    }
                    if (that.showbot) {
                        that.botrank = that.form4.getItem("botrank").getValue();
                    }
                    if (that.srank) {
                        that.steam = that.form4.getItem("steam").getValue();
                        that.steamr1 = that.form4.getItem("steamr1").getValue();
                        that.steamr2 = that.form4.getItem("steamr2").getValue();
                        if (that.steamr1 > that.steamr2) {
                            that.form4.getItem("steam").setProperties({
                                helpMessage: "输入有误，起始排名不应该超过终止排名",
                            });
                            alert("输入有误，起始排名不应该超过终止排名");
                            submitflag = false;
                        }
                    }
                    if (that.snext) {
                        const nteam = that.form4.getItem("nteam").getValue();
                        that.nteam1 = that.matchleft[nteam][0];
                        that.nteam2 = that.matchleft[nteam][1];
                    }
                    if (that.matchleftcnt <= 3) {
                        const realmatchleft = [];
                        if (that.matchleftcnt >= 1) {
                            const t = that.form4.getItem("mlseq1").getValue();
                            const t1 = that.matchleft[t][0];
                            const t2 = that.matchleft[t][1];
                            realmatchleft.push([t1, t2, that.matchleft[t][2]]);
                        }
                        if (that.matchleftcnt >= 2) {
                            const t = that.form4.getItem("mlseq2").getValue();
                            const t1 = that.matchleft[t][0];
                            const t2 = that.matchleft[t][1];
                            if (t == that.form4.getItem("mlseq1").getValue()) {
                                that.form4.getItem("mlseq2").setProperties({
                                    helpMessage: "输入有误，场次重复",
                                });
                                alert("输入有误，场次重复");
                                submitflag = false;
                            }
                            else {
                                that.form4.getItem("mlseq2").setProperties({
                                    helpMessage: null,
                                });
                                realmatchleft.push([t1, t2, that.matchleft[t][2]]);
                            }
                        }
                        if (that.matchleftcnt == 3) {
                            const t = that.form4.getItem("mlseq3").getValue();
                            const t1 = that.matchleft[t][0];
                            const t2 = that.matchleft[t][1];
                            if (t == that.form4.getItem("mlseq1").getValue() || t == that.form4.getItem("mlseq2").getValue()) {
                                that.form4.getItem("mlseq3").setProperties({
                                    helpMessage: "输入有误，场次重复",
                                });
                                alert("输入有误，场次重复");
                                submitflag = false;
                            }
                            else {
                                that.form4.getItem("mlseq3").setProperties({
                                    helpMessage: null,
                                });
                                realmatchleft.push([t1, t2, that.matchleft[t][2]]);
                            }
                        }
                        if (submitflag) {
                            that.matchleft = realmatchleft;
                        }
                    }

                    if (submitflag) {
                        const data = {
                            warning: "请勿随意修改文件内容，否则读取文件后可能导致系统出错",
                            teamcnt: that.teamcnt,
                            double: that.double,
                            bo: that.bo,
                            wscore: that.wscore,
                            lscore: that.lscore,
                            dscore: that.dscore,
                            teamnames: that.teamnames,
                            scoreboard: that.scoreboard,
                            matchleftcnt: that.matchleftcnt,
                            matchleft: that.matchleft,
                            showtop: that.showtop,
                            showbot: that.showbot,
                            toprank: that.toprank,
                            botrank: that.botrank,
                            sadd: that.sadd,
                            srank: that.srank,
                            snext: that.snext,
                            steam: that.steam,
                            steamr1: that.steamr1,
                            steamr2: that.steamr2,
                            nteam1: that.nteam1,
                            nteam2: that.nteam2,
                            mostml: that.mostml
                        }
                        that.form4.getItem("next").setProperties({
                            loading: true
                        });
                        that.form4.getItem("next").disable();
                        that.form4.getItem("pre").disable();
                        that.form4.getItem("reset").disable();
                        that.form4.getItem("errm3").setProperties({
                            label: "*计算中，耗时可能较长，请耐心等待",
                        });
                        //const start = Date.now();
                        $.ajax({
                            url: '/calculate',
                            type: 'POST',
                            data: data,
                            success: function (response) {
                                if (response.status === 'error') {
                                    alert("计算错误: " + response.message);
                                    that.form4.getItem("next").enable();
                                    that.form4.getItem("pre").enable();
                                    that.form4.getItem("reset").enable();
                                    that.form4.getItem("next").setProperties({
                                        loading: false
                                    });
                                }
                                else {
                                    //const end = Date.now();
                                    //console.log(`执行时间：${end - start} 毫秒`);
                                    const lines = response.res.split(/\r?\n/).filter(line => line.trim() !== '');
                                    const arrays = lines.map(line => JSON.parse(line));
                                    //console.log(arrays);
                                    that.maintabbar.enableTab("tab5");
                                    that.maintabbar.setActive("tab5");
                                    that.maintabbar.disableTab("tab4");
                                    that.init5(arrays, data);
                                }
                            },
                            error: function (jqXHR, textStatus, errorThrown) {
                                if (jqXHR.status == 500) {
                                    alert("抱歉，计算超时，请减少未进行比赛场次或队伍数量以简化计算！")
                                }
                                else {
                                    alert("服务器异常，请尝试刷新页面或重启系统！")
                                }
                                that.form4.getItem("next").enable();
                                that.form4.getItem("pre").enable();
                                that.form4.getItem("reset").enable();
                                that.form4.getItem("next").setProperties({
                                    loading: false
                                });
                            }
                        });
                    }
                    
                });
                this.form4.getItem("pre").events.on("click", function (events) {
                    that.maintabbar.enableTab("tab3");
                    that.maintabbar.setActive("tab3");
                    that.maintabbar.disableTab("tab4");
                    that.init3();
                });
                this.form4.getItem("reset").events.on("click", function (events) {
                    that.maintabbar.destructor();
                    that.init();
                });
            },
            init5(arrays, data) {
                const that = this;
                const addstr = this.bo == -1 ? "同分" : "加赛";
                var columns;
                this.dgrid_cur = new DataCollection;
                this.dgrid_pos = new DataCollection;
                this.dgrid_rank = new DataCollection;
                this.dgrid_srank = new DataCollection;
                this.dgrid_add = new DataCollection;
                this.dgrid_steam = new DataCollection;
                this.grid_nrank = [];
                this.dgrid_nrank = [];
                this.reslayout = new Layout(null, {
                    rows: [
                        {
                            id: "but",
                            height: "content",
                        },
                        {
                            id: "tab",
                        },
                        {
                            id: "info",
                            height: "content",
                        },
                    ],
                });
                this.maintabbar.getCell("tab5").attach(this.reslayout);
                this.resform = new Form(null, {
                    css: "dhx_widget--bordered",
                    cols: [
                        {
                            type: "button",
                            value: "上一步",
                            name: "pre",
                        },
                        {
                            type: "spacer",
                            width: 50
                        },
                        {
                            type: "button",
                            value: "重置",
                            name: "reset",
                        },
                        {
                            type: "spacer",
                            width: 50
                        },
                        {
                            type: "button",
                            value: "保存数据",
                            name: "save"
                        },
                        {
                            type: "spacer",
                            width: 50
                        },
                        {
                            type: "text",
                            name: "text",
                        }
                    ],
                });
                if (this.bo == -1) {
                    this.resform.getItem("text").setValue("自由得分赛制下，多支队伍同分时排名方法会根据具体赛事规则有所不同，此处只要积分相同就判定为同分，仅供参考。");
                }
                else {
                    this.resform.getItem("text").setValue("多支队伍同分时排名方法会根据具体赛事规则有所不同，此处按胜场>净胜分>相互比赛胜场>相互比赛净胜分排名。若以上规则无法区分排名先后，则判定为需要加赛。");
                }
                this.infoform = new Form(null, {
                    css: "dhx_widget--bordered",
                    cols: [
                        {
                            type: "text",
                            name: "info",
                        }
                    ],
                });
                const views = [{ tab: "当前排名", id: "cur" }];
                if (this.matchleftcnt > 0) {
                    if (this.matchleftcnt <= this.mostml) {
                        views.push(
                            { tab: "最终排名概率", id: "pos" }
                        )
                    }
                    else {
                        views.push(
                            { tab: "最终排名概率(蒙特卡洛模拟)", id: "pos" }
                        )
                    }
                    if (this.matchleftcnt <= 3) {
                        views.push(
                            { tab: "可能的排名情况(详细版)", id: "rank" },
                            { tab: "可能的排名情况(简化版)", id: "srank" },
                            { tab: "可能的排名情况(可视化)", id: "vrank" }
                        )
                    }
                    if (this.sadd) {
                        views.push(
                            { tab: addstr + "筛选", id: "add" }
                        )
                    }
                    if (this.srank) {
                        var stab = this.teamnames[this.steam] + "排名" + String(this.steamr1) + "-" + String(this.steamr2) + "情况筛选";
                        views.push(
                            { tab: stab, id: "steam" }
                        )
                    }
                    if (this.snext) {
                        if (this.bo == -1) {
                            const score = ["胜", "平", "负"];
                            for (let i = 0; i < 3; i++) {
                                var stab = this.teamnames[this.nteam1] + score[i] + this.teamnames[this.nteam2] + "时排名概率";
                                var sid = "nrank" + String(i + 1);
                                views.push(
                                    { tab: stab, id: sid },
                                )
                            }
                        }
                        else {
                            const score = [];
                            for (let i = 0; i < (this.bo + 1) / 2; i++) {
                                score[i] = [String((this.bo + 1) / 2), String(i)];
                                score[this.bo - i] = [String(i), String((this.bo + 1) / 2)];
                            }
                            for (let i = 0; i < (this.bo + 1); i++) {
                                var stab = this.teamnames[this.nteam1] + score[i][0] + ":" + score[i][1] + this.teamnames[this.nteam2] + "时排名概率";
                                var sid = "nrank" + String(i + 1);
                                views.push(
                                    { tab: stab, id: sid },
                                )
                            }
                        }
                        
                    }
                }
                this.restabbar = new Tabbar(null, {
                    mode: "top",
                    css: "dhx_widget--bordered",
                    views
                });
                this.reslayout.getCell("but").attach(this.resform);
                this.reslayout.getCell("tab").attach(this.restabbar);
                this.reslayout.getCell("info").attach(this.infoform);
                function getnextscores(arr) {
                    var scorestr = [];
                    for (let i = 0; i < arr.length; i++) {
                        var str = ""
                        for (let j = 0; j < arr[0].length; j++) {
                            if (that.bo != -1) {
                                str = str + that.teamnames[arr[i][j][0]] + String(arr[i][j][1]) + ":" + String(arr[i][j][2]) + that.teamnames[arr[i][j][3]];
                            }
                            else {
                                if (arr[i][j][1] == 1) {
                                    str = str + that.teamnames[arr[i][j][0]] + "胜" + that.teamnames[arr[i][j][3]];
                                }
                                else if (arr[i][j][2] == 1) {
                                    str = str + that.teamnames[arr[i][j][0]] + "负" + that.teamnames[arr[i][j][3]];
                                }
                                else {
                                    str = str + that.teamnames[arr[i][j][0]] + "平" + that.teamnames[arr[i][j][3]];
                                }
                            }
                            if (j < arr[0].length - 1) {
                                str = str + ", ";
                            }
                        }
                        scorestr.push(str);
                    }
                    return scorestr
                }
                function getaddstr(arr) {
                    var adds = "";
                    for (let i = 0; i < arr.length; i++) {
                        for (let j = 0; j < arr[i].length; j++) {
                            adds = adds + that.teamnames[arr[i][j]];
                            if (j < arr[i].length - 1) {
                                adds = adds + ",";
                            }
                        }
                        adds = adds + addstr;
                        if (i < arr.length - 1) {
                            adds = adds + ", ";
                        }
                    }
                    if (arr.length == 0) {
                        adds = "无";
                    }
                    return adds
                }
                function createcolumnsofrank(type) {
                    const str = type == 0 ? "排名" : "所有可能的赛果";
                    const columns = [
                        {
                            adjust: true,
                            id: "index",
                            header: [{ text: str }],
                        },
                        {
                            adjust: true,
                            id: "team",
                            header: [{ text: "战队" }],
                        },
                    ];
                    if (that.bo == -1) {
                        columns.push(
                            {
                                adjust: true,
                                id: "w_d_l",
                                header: [{ text: "胜-平-负" }],
                            },
                            {
                                adjust: true,
                                id: "score",
                                header: [{ text: "积分" }],
                            },
                            {
                                adjust: true,
                                id: "netscore",
                                header: [{ text: "净胜分" }],
                            },
                            {
                                adjust: true,
                                id: "totalscore",
                                header: [{ text: "总得分" }],
                            },
                        );
                    }
                    else {
                        columns.push(
                            {
                                adjust: true,
                                id: "w_l",
                                header: [{ text: "胜-负" }],
                            },
                            {
                                adjust: true,
                                id: "netscore",
                                header: [{ text: "净胜分" }],
                            },
                        );
                    }
                    return columns
                }
                function createcolumnsofsrank() {
                    const columns = [
                        {
                            adjust: true,
                            id: "index",
                            header: [{ text: "所有可能的赛果" }],
                        }
                    ]
                    for (let i = 0; i < that.teamcnt; i++) {
                        columns.push(
                            {
                                adjust: true,
                                id: String(i + 1),
                                header: [{ text: String(i + 1) }],
                            }
                        )
                    }
                    columns.push(
                        {
                            adjust: true,
                            id: "add",
                            header: [{ text: addstr }],
                        }
                    )
                    return columns
                }
                function createcolumnsofpos() {
                    const columns = [
                        {
                            adjust: true,
                            id: "team",
                            header: [{ text: "战队" }],
                        },
                    ];
                    for (let i = 0; i < that.teamcnt; i++) {
                        columns.push(
                            {
                                adjust: true,
                                id: String(i + 1),
                                header: [{ text: String(i + 1) }],
                            }
                        )

                    }
                    columns.push(
                        {
                            adjust: true,
                            id: "add",
                            header: [{ text: addstr }],
                        }
                    )
                    if (that.showtop) {
                        columns.push(
                            {
                                adjust: true,
                                id: "top",
                                header: [{ text: "排名前" + String(that.toprank) }],
                            }
                        )
                    }
                    if (that.showbot) {
                        columns.push(
                            {
                                adjust: true,
                                id: "bot",
                                header: [{ text: "排名后" + String(that.teamcnt - that.botrank + 1) }],
                            }
                        )
                    }
                    return columns
                }
                columns = createcolumnsofrank(0);
                this.grid_cur = new Grid(null, {
                    data: this.dgrid_cur,
                    sortable: false,
                    columns
                });
                for (let i = 0; i < this.teamcnt; i++) {
                    if (this.bo == -1) {
                        this.dgrid_cur.add(
                            {
                                index: i + 1,
                                team: this.teamnames[arrays[0][i][0]],
                                w_d_l: arrays[0][i][1],
                                score: arrays[0][i][2],
                                netscore: arrays[0][i][3],
                                totalscore: arrays[0][i][5],
                            }
                        );
                    }
                    else {
                        this.dgrid_cur.add(
                            {
                                index: i + 1,
                                team: this.teamnames[arrays[0][i][0]],
                                w_l: arrays[0][i][1],
                                netscore: arrays[0][i][3],
                            }
                        );
                    }
                }
                this.restabbar.getCell("cur").attach(this.grid_cur);
                var curinfo = addstr + "情况：";
                if (this.matchleftcnt == 0) {
                    curinfo += getaddstr(arrays[1]);
                }
                else {
                    curinfo += "未完赛，无法判断，若有同分暂时按队伍序号排序";
                }
                this.infoform.getItem("info").setValue(curinfo);
                if (this.matchleftcnt > 0) {
                    this.vposlayout = new Layout(null, {
                        cols: [
                            {
                                id: "grid",
                                header: "表格形式",
                                resizable: true
                            },
                            {
                                id: "chart",
                                header: "可视化",
                                width: 500,
                            },
                        ],
                    });
                    columns = createcolumnsofpos();
                    this.grid_pos = new Grid(null, {
                        data: this.dgrid_pos,
                        sortable: false,
                        columns
                    });
                    for (let i = 0; i < this.teamcnt; i++) {
                        const add = {
                            team: this.teamnames[i],
                            add: String(arrays[2][i][this.teamcnt]) + "%",
                        }
                        for (let j = 0; j < this.teamcnt; j++) {
                            add[String(j + 1)] = String(arrays[2][i][j]) + "%";
                        }
                        if (this.showtop) {
                            add["top"] = String(arrays[2][i][this.teamcnt + 1]) + "%";
                            if (this.showbot) {
                                add["bot"] = String(arrays[2][i][this.teamcnt + 2]) + "%";
                            }
                        }
                        else if (this.showbot) {
                            add["bot"] = String(arrays[2][i][this.teamcnt + 1]) + "%";
                        }
                        this.dgrid_pos.add(add);
                    }
                    this.restabbar.getCell("pos").attach(this.vposlayout);
                    this.vposlayout.getCell("grid").attach(this.grid_pos);
                        
                    if (this.matchleftcnt <= 3) {
                        const allscores = getnextscores(arrays[3]);
                        columns = createcolumnsofrank(1)
                        this.grid_rank = new Grid(null, {
                            data: this.dgrid_rank,
                            sortable: false,
                            columns
                        });
                        for (let i = 0; i < arrays[3].length; i++) {
                            const adds = getaddstr(arrays[4][i][this.teamcnt]);
                            if (this.bo == -1) {
                                this.dgrid_rank.add(
                                    {
                                        index: allscores[i],
                                        team: "-----",
                                        w_d_l: "-----",
                                        score: "-----",
                                        netscore: "-----",
                                        totalscore: "-----",
                                    }
                                )
                                for (let j = 0; j < this.teamcnt; j++) {
                                    this.dgrid_rank.add(
                                        {
                                            index: j + 1,
                                            team: this.teamnames[arrays[4][i][j][0]],
                                            w_d_l: arrays[4][i][j][1],
                                            score: arrays[4][i][j][2],
                                            netscore: arrays[4][i][j][3],
                                            totalscore: arrays[4][i][j][5],
                                        }
                                    )
                                }
                                this.dgrid_rank.add(
                                    {
                                        index: addstr,
                                        team: adds,
                                        w_d_l: null,
                                        score: null,
                                        netscore: null,
                                        totalscore: null,
                                    }
                                )
                            }
                            else {
                                this.dgrid_rank.add(
                                    {
                                        index: allscores[i],
                                        team: "-----",
                                        w_l: "-----",
                                        netscore: "-----",
                                    }
                                )
                                for (let j = 0; j < this.teamcnt; j++) {
                                    this.dgrid_rank.add(
                                        {
                                            index: j + 1,
                                            team: this.teamnames[arrays[4][i][j][0]],
                                            w_l: arrays[4][i][j][1],
                                            netscore: arrays[4][i][j][3],
                                        }
                                    )
                                }
                                this.dgrid_rank.add(
                                    {
                                        index: addstr,
                                        team: adds,
                                        w_l: null,
                                        netscore: null,
                                    }
                                )
                            }
                        }
                        this.restabbar.getCell("rank").attach(this.grid_rank);
                        columns = createcolumnsofsrank();
                        this.grid_srank = new Grid(null, {
                            data: this.dgrid_srank,
                            sortable: false,
                            columns
                        });
                        for (let i = 0; i < arrays[3].length; i++) {
                            var adds = getaddstr(arrays[5][i][this.teamcnt]);
                            const add = {
                                index: allscores[i],
                                add: adds,
                            }
                            for (let j = 0; j < this.teamcnt; j++) {
                                add[String(j + 1)] = this.teamnames[arrays[5][i][j]];
                            }
                            this.dgrid_srank.add(add);
                        }
                        this.restabbar.getCell("srank").attach(this.grid_srank);

                        this.restabbar.getCell("vrank").attachHTML(`
                            <div class="mermaid-wrap">
                                <div id="mermaid-target"></div>
                            </div>
                        `);
                    }
                    if (this.sadd) {
                        const addscores = getnextscores(arrays[6]);
                        columns = createcolumnsofsrank();
                        this.grid_add = new Grid(null, {
                            data: this.dgrid_add,
                            sortable: false,
                            columns
                        });
                        for (let i = 0; i < arrays[6].length; i++) {
                            var adds = getaddstr(arrays[7][i][this.teamcnt]);
                            const add = {
                                index: addscores[i],
                                add: adds,
                            }
                            for (let j = 0; j < this.teamcnt; j++) {
                                add[String(j + 1)] = this.teamnames[arrays[7][i][j]];
                            }
                            this.dgrid_add.add(add);
                        }
                        this.restabbar.getCell("add").attach(this.grid_add);
                    }
                    if (this.srank) {
                        const srankscores = getnextscores(arrays[8]);
                        columns = createcolumnsofsrank();
                        this.grid_steam = new Grid(null, {
                            data: this.dgrid_steam,
                            sortable: false,
                            columns
                        });
                        for (let i = 0; i < arrays[8].length; i++) {
                            var adds = getaddstr(arrays[9][i][this.teamcnt]);
                            const add = {
                                index: srankscores[i],
                                add: adds,
                            }
                            for (let j = 0; j < this.teamcnt; j++) {
                                add[String(j + 1)] = this.teamnames[arrays[9][i][j]];
                            }
                            this.dgrid_steam.add(add);
                        }
                        this.restabbar.getCell("steam").attach(this.grid_steam);
                    }
                    if (this.snext) {
                        const maxi = this.bo == -1 ? 3 : this.bo + 1;
                        for (let i = 0; i < maxi; i++) {
                            this.dgrid_nrank[i] = new DataCollection;
                            columns = createcolumnsofpos();
                            this.grid_nrank[i] = new Grid(null, {
                                data: this.dgrid_nrank[i],
                                sortable: false,
                                columns
                            });
                            for (let j = 0; j < this.teamcnt; j++) {
                                const add = {
                                    team: this.teamnames[j],
                                    add: String(arrays[10 + i][j][this.teamcnt]) + "%",
                                }
                                for (let k = 0; k < this.teamcnt; k++) {
                                    add[String(k + 1)] = String(arrays[10 + i][j][k]) + "%";
                                }
                                if (this.showtop) {
                                    add["top"] = String(arrays[10 + i][j][this.teamcnt + 1]) + "%";
                                    if (this.showbot) {
                                        add["bot"] = String(arrays[10 + i][j][this.teamcnt + 2]) + "%";
                                    }
                                }
                                else if (this.showbot) {
                                    add["bot"] = String(arrays[10 + i][j][this.teamcnt + 1]) + "%";
                                }
                                this.dgrid_nrank[i].add(add);
                            }
                            this.restabbar.getCell("nrank" + String(i + 1)).attach(this.grid_nrank[i]);
                        }  
                    }
                }
                
                this.restabbar.events.on("change", function (id, prev) {
                    if (id == "cur") {
                        that.infoform.getItem("info").setValue(curinfo);
                    }
                    else if (id == "pos" || id.startsWith("nrank")) {
                        if (that.bo == -1) {
                            that.infoform.getItem("info").setValue("假设后续每场比赛双方胜/平/负概率相等，若有同分，假设按其他规则决定排名后，同分的各支队伍排在任意名次的概率相等");
                        }
                        else {
                            that.infoform.getItem("info").setValue("假设后续每场比赛出现每种比分概率相等，若有加赛，假设参与加赛的所有队伍在加赛中取得任意名次的概率相等");
                        }
                        that.grid_pos.events.on("cellMouseOver", (row, column, event) => {
                            var i = 0;
                            var dataset = [];
                            while (that.teamnames[i] != row.team) {
                                i++;
                            }
                            for (let j = 0; j < that.teamcnt; j++) {
                                dataset.push(
                                    { rank: String(j + 1), value: arrays[2][i][j]}
                                );
                            }
                            dataset.push(
                                { rank: addstr, value: arrays[2][i][that.teamcnt]}
                            );
                            const config = {
                                type: "pie3D",
                                css: "dhx_widget--bg_white dhx_widget--bordered",
                                series: [
                                    {
                                        value: "value",
                                        stroke: "#FFFFFF",
                                        strokeWidth: 2,
                                        subType: "percentOnly",
                                    }
                                ],
                                legend: {
                                    values: {
                                        text: "rank",
                                    },
                                    halign: "right",
                                    valign: "top"
                                }
                            };
                            that.chart = new Chart(null, config);
                            that.chart.data.parse(dataset);
                            that.vposlayout.getCell("chart").attach(that.chart);
                        });
                    }
                    else {
                        that.infoform.getItem("info").setValue(null);
                        if (id == "vrank") {
                            setTimeout(() => {
                                that.initMermaid(arrays[5]);
                            }, 50);
                        }
                    }
                });

                this.resform.getItem("save").events.on("click", async function (events) {
                    try {
                        if ('showSaveFilePicker' in window) {
                            const handle = await window.showSaveFilePicker({
                                suggestedName: `calculation_${new Date().getTime()}.json`,
                                types: [{
                                    description: 'JSON Files',
                                    accept: { 'application/json': ['.json'] }
                                }]
                            });

                            const writable = await handle.createWritable();
                            await writable.write(JSON.stringify(data));
                            await writable.close();
                        } else {
                            const blob = new Blob([JSON.stringify(data)], { type: "application/json" });
                            const url = URL.createObjectURL(blob);

                            const a = document.createElement("a");
                            a.href = url;
                            a.download = `calculation_${new Date().getTime()}.json`;
                            document.body.appendChild(a);
                            a.click();
                            document.body.removeChild(a);
                            URL.revokeObjectURL(url);
                        }
                    } catch (err) {
                        if (err.name !== 'AbortError') {
                            alert(`保存失败: ${err.message}`);
                        }
                    }
                });

                this.resform.getItem("pre").events.on("click", function (events) {
                    that.maintabbar.enableTab("tab4");
                    that.maintabbar.setActive("tab4");
                    that.maintabbar.disableTab("tab5");
                    that.init4();
                });
                this.resform.getItem("reset").events.on("click", function (events) {
                    that.maintabbar.destructor();
                    that.init();
                });
            },
            initMermaid(arr) {
                const that = this;
                const addstr = this.bo == -1 ? "同分" : "加赛";
                const bo_ = this.bo == -1 ? 3 : this.bo + 1;
                mermaid.initialize({
                    theme: 'forest',
                    startOnLoad: false,
                    flowchart: {
                        nodeSpacing: 10,
                        rankSpacing: 250,
                        curve: 'stepAfter',
                    }
                });
                function getaddstr0(arr) {
                    var adds = "";
                    for (let i = 0; i < arr.length; i++) {
                        for (let j = 0; j < arr[i].length; j++) {
                            adds = adds + that.teamnames[arr[i][j]];
                            if (j < arr[i].length - 1) {
                                adds = adds + ",";
                            }
                        }
                        adds = adds + addstr;
                        if (i < arr.lengt - 1) {
                            adds = adds + ",";
                        }
                    }
                    if (arr.length == 0) {
                        adds = "无" + addstr;
                    }
                    return adds
                }
                const vs = [];
                var bf;
                const rankstr = [];
                for (let i = 0; i < this.matchleftcnt; i++) {
                    vs.push("[" + this.teamnames[this.matchleft[i][0]] + " VS " + this.teamnames[this.matchleft[i][1]] + "]");
                }
                if (this.bo == -1) {
                    bf = ["|胜|", "|平|", "|负|"];
                }
                else {
                    bf = [];
                    for (let i = 0; i < bo_ / 2; i++) {
                        bf[i] = "|" + String(bo_ / 2) + ":" + String(i) + "|";
                        bf[this.bo - i] = "|" + String(i) + ":" + String(bo_ / 2) + "|";
                    }
                }
                for (let i = 0; i < arr.length; i++) {
                    var str = "";
                    for (let j = 0; j < this.teamcnt; j++) {
                        str = str + this.teamnames[arr[i][j]];
                        if (j < this.teamcnt - 1) {
                            str = str + ",";
                        }
                    }
                    str = str + "\n" + getaddstr0(arr[i][this.teamcnt]);
                    rankstr.push(str);
                }
                var ind = 0;
                var diagram = "graph LR \n A0" + vs[0] + "\n";
                var numb = (bo_ ** this.matchleftcnt - 1) / (bo_ - 1);
                function getcode(i, n) {
                    var bg = i * bo_ + 1;
                    var str = "A" + String(i);
                    if (n < that.matchleftcnt) {
                        for (let j = 0; j < bo_; j++) {
                            var stn = "A" + String(bg + j);
                            diagram = diagram + str + " --> " + bf[j] + " " + stn + vs[n] + " \n ";
                            getcode(bg + j, n + 1);
                        }
                    }
                    else {
                        for (let j = 0; j < bo_; j++) {
                            var stn = "A" + String(bg + j);
                            diagram = diagram + str + " --> " + bf[j] + " " + stn + "[" + rankstr[bg + j - numb] + "]" + " \n ";
                        }
                    }
                }
                getcode(0, 1);
                const container = document.getElementById('mermaid-target');

                const mermaidId = 'mermaid-diagram-' + Date.now();

                mermaid.render(mermaidId, diagram)
                    .then(({ svg }) => {
                        container.innerHTML = svg;
                    })
                    .catch(err => {
                        console.error('Mermaid 渲染失败:', err);
                    });
            },
        }
    };
</script>

<style>
    @import "dhx-suite/codebase/suite.min.css";

    .mermaid-wrap {
        height: 100%;
        overflow: hidden;
        position: relative;
    }

    #mermaid-target {
        width: 100%;
        height: 100%;
        overflow: auto;
        padding: 20px;
        background: #fff;
        border-radius: 4px;
    }
</style>
