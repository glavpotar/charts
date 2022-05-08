<h2 align="center">Stock chart with FastApi and Highcharts JS</h2>
<div align="center"><img src="demo.png" width=90% height=115%></div>

<br><br>

<h2>Requirements</h2>
<ul>
    <li>PostgreSQL 14.2</li>
    <li>Python 3.10.4</li>
    <ul>
        <li>libs : 'requirements.txt'</li>
    </ul>
</ul>

<br><br>

<h2>Database structure</h2>
<h3>Columns</h3>
<ul>
    <li>id - ()int. type - identity</li>
    <li>time_received - charvar</li>
    <li>price - charvar</li>
</ul>
<div align="center"><img src="db_demo.png"></div>

<br><br>

<h2>Usage</h2>
<h4>as long as uvicorn have troubles running asynchronously,
    we have to run "main.py" and "headapi.py" separately</h4>
    <ul>
    <li>run "main.py"</li>
    <li>run "headapi.py"</li>
        <ul>
        <li>127.0.0.1:8220 by default</li>
        </ul>
    </ul>
