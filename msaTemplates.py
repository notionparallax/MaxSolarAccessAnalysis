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
    <h1>Run at {{ when }}</h1>
    <table>
  ''')

eachimgTempl = Template(u'''\    
<tr>       
    
        {%- for img in row %} 
        {% if loop.first %} 
            <td class="row-title">
                <div class"info-box">
                    <p class="month">{{monthNames[img.month]}}</p>
                    <p>level: {{img.building_level}}</p>
                    <p>Appt: {{img.appartment}}</p>
                </div>
            </td>
        {% endif %}    
        <td class="render appt-{{img.appartment}} level-{{img.building_level}}" data-percentWhite="{{img.pcWhite}}">
            <p><img src="{{img.path}}/{{ img.filename }}" title="|{{ '{0:0>2}'.format(img.pcWhite)}}| {{ img.hour }}:{{ '{0:0>2}'.format(img.minute) }} - {{ img.filename }}" /></p>
            
            <p class="time">{{ img.hour }}:{{ '{0:0>2}'.format(img.minute) }} {{ '{0:0>2}'.format(img.pcWhite)}}</p>
        <td>            
        {% if loop.last %} 
            <td class="row-title {{window['passStatus']}}">
                <div class"info-box">
                    <h1 class="pass-status">{{window['passStatus']}}</h1>
                    <p>Total Hours: {{window['totalHours']}}</p>
                    <p>Bracket Hours: {{window['inBracketHours']}}</p>
                </div>
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