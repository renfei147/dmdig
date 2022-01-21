data = {}
initChart();
wordcloud = new Js2WordCloud(document.getElementById('wordcloud'))
$("button#submit").click(function () {
    var video_id = $("input#video-id").val();
    if (video_id == "") return;
    $("body").loading({ message: "加载中...<br> 如果视频较长，这可能需要一段时间" });
    $("button#submit").prop("disabled", true);
    $.get("/api/bilibili/" + video_id).done(function (res) {
        if (res.success) {
            data = res;
            drawChart();
            drawWordcloud(0, data.slices.length - 1);
        } else {
            alert(res.message);
        }
        $("body").loading("stop");
        $("button#submit").prop("disabled", false);
    });
});
function initChart() {
    chart = echarts.init(document.getElementById('chart'));
    var option = {
        xAxis: {
            name: '时间',
            data: []
        },
        yAxis: {
            name: '弹幕量'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross'
            }
        },
        toolbox: {
            show: true,
            feature: {
                saveAsImage: {},
                dataView: {},
                dataZoom: {},
            }
        },
        dataZoom: [
            {
                type: "slider"
            }
        ],
        grid: {
            x: 50,
            y: 50,
            x2: 50,
            y2: 50
        },
        series: [
            {
                name: '弹幕量',
                data: [],
                type: 'line',
                smooth: true,
                showSymbol: false
            }
        ]
    };
    chart.setOption(option);
    chart.on("datazoom", function (params) {
        var length = data.slices.length;
        var first = Math.ceil(params.start / 100 * length);
        var last = Math.floor(params.end / 100 * length)
        drawWordcloud(first, last);
    });
}
function drawWordcloud(first, last) {
    var allword = {};
    for (var i = first; i <= last; i++) {
        for (word in data.slices[i].w) {
            if (word in allword) {
                allword[word] += data.slices[i].w[word];
            } else {
                allword[word] = data.slices[i].w[word];
            }
        }
    }
    var list = [];
    for (word in allword) {
        list.push([word, allword[word]]);
    }
    wordcloud.setOption({
        tooltip: {
            show: true
        },
        list: list
    })
}
function drawChart() {
    var timeseq = [], nseq = [];
    var sl = data.slice_length;
    for (var i = 0; i < data.slices.length; i++) {
        timeseq.push(timeformat(sl * i + sl / 2));
        nseq.push(data.slices[i].n)
    }

    var option = {
        xAxis: {
            name: '时间',
            data: timeseq
        },
        series: [
            {
                name: '弹幕量',
                data: nseq,
            }
        ]
    };
    chart.setOption(option);
}
function timeformat(second) {
    var mimute = Math.floor(second / 60);
    second = second - mimute * 60;
    return ("0" + mimute).slice(-2) + ":" + ("0" + second).slice(-2);
}