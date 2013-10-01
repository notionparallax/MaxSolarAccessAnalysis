from jinja2 import Template

headTmpl = Template(u'''\
<!DOCTYPE html>
<html>
  <head>
    <title>{{ variable|escape }}</title>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script> 
    <script src="chroma.js/chroma.min.js"></script>
    <style>
        img {height:60px;
             border-right-style: solid;
             border-right-width: 1px;
             border-right-color: #C0C0C0}
        .render{width:225px; }
        body{font-family:'HelveticaNeueLT Com 45 Lt', 'Helvetica', Arial}
    </style>
  </head>
  <body>
    <h1>Run at {{ when }}</h1>
  ''')


eachTableTempl = Template(u'''\
    <h1>{{monthName}} 21<sup>st</sup></h1>
    <table>
        <tr>
            {%- for img in amoi[0] %}
                <td>
                    <p>{{ img.hour }}:{{ '{:2}'.format(img.minute) }}</p>
                <td>
            {%- endfor %}
        </tr>
        <tr>
            {%- for img in amoi[0] %}
                <td>
                    <div class="render" data-percentWhite="{{img.pcWhite}}">
                        <p>{{ img.name|replace("-", " ") }}<br>
                        <img src="{{img_path}}/{{ img.fileName }}" /></p>
                    </div>
                <td>
            {%- endfor %}
        </tr>
        <tr>
            {%- for img in amoi[0] %}
                <td>
                    <div class="render" data-percentWhite="{{img.pcWhite}}">
                        <p>{{ amoi[1][loop.index-1].name|replace("-", " ") }}<br>                  
                            <img src="{{img_path}}/{{ amoi[1][loop.index-1].fileName }}" /><img src="{{img_path}}/{{ amoi[2][loop.index-1].fileName }}" />
                        </p>
                    </div>
                <td>
            {%- endfor %}
        </tr>
    </table>
''')

tailTmpl = Template(u'''\
        <h3>Disclaimer</h3>
        <p>{{ variable|escape }}</p>
        <script>
        $(document).ready(function(){
            console.log("I'm in UR jq");
            var scale = chroma.scale(['white', 'red']);            
            $('.render').each(function(){
                var pc = $(this).data("percentwhite");
                var col = scale(pc).hex();                
                $(this).css("background-color", col);
            });
        });
        </script>
    </body>
</html>''')