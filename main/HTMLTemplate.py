# -*- coding: utf-8 -*-
from string import Template

wordRowHTML = """
<tr>
    <td>${td1}</td>
    <td>${td2}</td>
    <td>${td3}</td>
    <td>${td4}</td>
</tr>
"""

rowTemplate = Template(wordRowHTML)

tableHTML = """
<table class="ui single line table">
<thead>
    <tr>
        <th>单词</th>
        <th>中文</th>
        <th>出现的年份</th>
        <th>得分</th>
    </tr>
    </thead>
    $content
</table>
"""

tableTemplate = Template(tableHTML)


totalTable = """
<table class="ui single line table">
<thead>
    <tr>
        <th>单词</th>
        <th>中文</th>
        <th>单词</th>
        <th>中文</th>
    </tr>
    </thead>
    $content
</table>
"""
totalTemplate = Template(totalTable)



