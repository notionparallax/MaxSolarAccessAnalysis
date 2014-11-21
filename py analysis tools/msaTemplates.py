from jinja2 import Template

headTmpl = Template(u'''\
<!DOCTYPE html>
<html>
  <head>
    <title>{{ variable|escape }}</title>
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script> 
    <script src="chroma.js/chroma.min.js"></script>
    <link rel="stylesheet" type="text/css" href="style.css">    
  </head>
  <body>
    <h1>Run on {{ when }}</h1>
    <table>
  ''')

eachimgTempl = Template(u'''\    
<tr>    
    {%- for img in row %} 
        {% if loop.first %} 
            <td class="info-box month">
                <!-- {{monthNames[img.month]}} -->
                level: {{img.name.split("-")[1]}}
            </td>
            <td class="info-box">                
                Appt:  {{img.name.split("-")[2]}}                
            </td>
            <td class="info-box">
                Win:   {{img.name.split("-")[3]}}
            </td>
        {% endif %}    
    <td class="render appt-{{img.appartment}} level-{{img.building_level}}" data-percentWhite="{{img.pcWhite}}">
        <p><img src="{{img.path}}/{{ img.filename }}" title="|{{ '{0:0>2}'.format(img.pcWhite)}}| {{ img.hour }}:{{ '{0:0>2}'.format(img.minute) }} - {{ img.filename }}" /></p>
        
        <span class="time">{{ img.hour }}:{{ '{0:0>2}'.format(img.minute) }}</span> <span class="pc-white">{{ '{0:0>2}'.format(img.pcWhite)}}</span>
    </td>            
        {% if loop.last %} 
            <td class="{{window['passStatus']}} info-box">                
                <h1 class="pass-status">{{window['passStatus']}}</h1>
            </td>
            <td class="info-box">
                <p>Total Hours: {{window['totalHours']}}</p>
            </td>
            <td class="info-box">
                <p>Bracket Hours: {{window['inBracketHours']}}</p>                
            </td>
        {% endif %}
    {%- endfor %}    
</tr>    
''')

tailTmpl = Template(u'''\
        </table>
        <h3>Disclaimer</h3>
        <p>{{ variable|escape }}</p>
        <script>
        $(document).ready(function(){
            console.log("I'm in UR jq");
            var scale = chroma.scale(['white', '#EFDEC1', '#605A41'])
                        .correctLightness(true);            
            $('.render').each(function(){
                var pc = $(this).data("percentwhite");
                var col = scale(pc).hex();                
                $(this).css("background-color", col);
            });
        });
        </script>
    </body>
</html>''')