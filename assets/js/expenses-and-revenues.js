


let myData = (country_id) => {
    let url = '/api/budgets/expense_revenue/?country_id=' + country_id;
    $.get(url, function (data) {

        console.log(data);
        expenses_and_revenues(data)


    }).fail(function () {
        console.log("Error on fetching budget basic info.");
    });
}

function expenses_and_revenues(_data) {
    am4core.ready(function () {

        // Themes begin
        am4core.useTheme(am4themes_animated);

        var chart = am4core.create('chartdiv', am4charts.XYChart)
        // chart.colors.step = 2;
        chart.colors.list = [
            am4core.color("#0F69A3"),
            am4core.color("#98B8DA"),
            am4core.color("#C90000"),
            am4core.color("#FF8080")
        ];
        chart.legend = new am4charts.Legend()
        // chart.legend.position = 'top'
        chart.legend.paddingTop = 40
        chart.legend.labels.template.maxWidth = 95
        chart.numberFormatter.bigNumberPrefixes = [
            { "number": 1e+3, "suffix": "K" },
            { "number": 1e+6, "suffix": "Mi" },
            { "number": 1e+9, "suffix": "Bi" },
            { "number": 1e+12, "suffix": "Tri" },
            { "number": 1e+15, "suffix": "Qua" }
            /*{"number": 1e+18, "suffix": "E"},
            {"number": 1e+21, "suffix": "Z"},
            {"number": 1e+24, "suffix": "Y"}*/
        ]

        var xAxis = chart.xAxes.push(new am4charts.CategoryAxis())
        xAxis.dataFields.category = 'year'
        xAxis.renderer.cellStartLocation = 0.1
        xAxis.renderer.cellEndLocation = 0.9
        xAxis.renderer.grid.template.location = 0;
        xAxis.numberFormatter = new am4core.NumberFormatter();
        xAxis.numberFormatter.numberFormat = "###";

        var yAxis = chart.yAxes.push(new am4charts.ValueAxis());
        yAxis.min = 0;
        yAxis.numberFormatter.numberFormat = "#. a";

        xAxis.renderer.grid.template.disabled = true;
        yAxis.renderer.grid.template.disabled = true;


        function createSeries(field, name, width, dx, dy) {
            var series = chart.series.push(new am4charts.ColumnSeries());
            series.dataFields.valueY = field;
            series.dataFields.categoryX = "year";
            series.name = name;
            series.columns.template.tooltipText = "{name}: [bold]{valueY}[/]";
            series.clustered = false;
            series.dx = dx;
            series.columns.template.width = width;

            // Tooltip
            series.columns.template.tooltipText = `[bold]Ano: {year.formatNumber('###')}[/]
            [bold]{currency}: {valueY.formatNumber('#,###')}[/]
            ${name} de acordo com grupamento {expense_group}`;

            // Label
            var bullet = series.bullets.push(new am4charts.LabelBullet());
            bullet.interactionsEnabled = false;
            bullet.dy = dy;
            bullet.dx = dx;
            bullet.fontSize = 12;
            bullet.label.verticalCenter = 'top';
            bullet.label.text = "{valueY.formatNumber('#.# a')}";
            bullet.label.fill = dy > 0 ? am4core.color('#FFF') : am4core.color('#000');
            bullet.label.truncate = false;
        }

        chart.data = _data;
        chart.maskBullets = false;



        createSeries("revenue_budget", "Dotação Despesa", 60, -40, -25);
        createSeries("revenue_execution", "Execução Despesa", 40, -40, 10);
        createSeries("expense_budget", "Dotação Receita", 60, 40, -25);
        createSeries("expense_execution", "Execução Receita", 40, 40, 10);

        function arrangeColumns() {

            var series = chart.series.getIndex(0);

            var w = 1 - xAxis.renderer.cellStartLocation - (1 - xAxis.renderer.cellEndLocation);
            if (series.dataItems.length > 1) {
                var x0 = xAxis.getX(series.dataItems.getIndex(0), "categoryX");
                var x1 = xAxis.getX(series.dataItems.getIndex(1), "categoryX");
                var delta = ((x1 - x0) / chart.series.length) * w;
                if (am4core.isNumber(delta)) {
                    var middle = chart.series.length / 2;

                    var newIndex = 0;
                    chart.series.each(function (series) {
                        if (!series.isHidden && !series.isHiding) {
                            series.dummyData = newIndex;
                            newIndex++;
                        }
                        else {
                            series.dummyData = chart.series.indexOf(series);
                        }
                    })
                    var visibleCount = newIndex;
                    var newMiddle = visibleCount / 2;

                    chart.series.each(function (series) {
                        var trueIndex = chart.series.indexOf(series);
                        var newIndex = series.dummyData;

                        var dx = (newIndex - trueIndex + middle - newMiddle) * delta

                        series.animate({ property: "dx", to: dx }, series.interpolationDuration, series.interpolationEasing);
                        series.bulletsContainer.animate({ property: "dx", to: dx }, series.interpolationDuration, series.interpolationEasing);
                    })
                }
            }
        }

    }); // end am4core.ready()
}


myData(country_id);