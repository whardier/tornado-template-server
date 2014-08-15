<!DOCTYPE html>
<!--[if lt IE 7 ]><html class="ie ie6" lang="en"> <![endif]-->
<!--[if IE 7 ]><html class="ie ie7" lang="en"> <![endif]-->
<!--[if IE 8 ]><html class="ie ie8" lang="en"> <![endif]-->
<!--[if (gte IE 9)|!(IE)]><!--><html lang="en"> <!--<![endif]-->

    <head>
        
        <meta charset="utf-8"/>
        
        <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
        <meta name="viewport" content="width=device-width, initial-scale=1"/>
        <meta name="description" content=""/>
        <meta name="author" content=""/>
        
        <title>{{ template_vars.get('name', 'Missing template_vars["name"]') }}</title>
        
        <!-- Bootstrap core CSS -->
        <link href="//cdnjs.cloudflare.com/ajax/libs/bootswatch/3.2.0+1/united/bootstrap.min.css" rel="stylesheet"/>

        <!-- FontAwesome Icons -->
        <link href="//cdnjs.cloudflare.com/ajax/libs/font-awesome/4.1.0/css/font-awesome.min.css" rel="stylesheet" />
        
        <link href="{{ static_url('css/test.css') }}" rel="stylesheet"/>
        
        <link rel="icon" href="{% module static_file_data_uri_base64('img/favicon.png') %}"/>

    </head>
    
    <body>
        
 <!-- Navigation -->
    <nav class="navbar navbar-default navbar-fixed-top" role="navigation">
        <div class="container">
            <!-- Brand and toggle get grouped for better mobile display -->
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="{{ reverse_url('template', 'test.html') }}">{{ template_vars.get('brand', 'Missing template_vars["brand"]') }}</a>
            </div>
            <!-- Collect the nav links, forms, and other content for toggling -->
            <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                <ul class="nav navbar-nav navbar-right">
                    <li>
                        <a href="https://github.com/whardier/tornado-template-server"><i class="fa fa-github"></i></a>
                    </li>
                    <li>
                        <a href="https://facebook.com/whardier"><i class="fa fa-facebook"></i></a>
                    </li>
                </ul>
            </div>
            <!-- /.navbar-collapse -->
        </div>
        <!-- /.container -->
    </nav>

    <header id="myCarousel" class="carousel slide">
        <!-- Indicators -->
        <ol class="carousel-indicators">
            <li data-target="#myCarousel" data-slide-to="0" class="active"></li>
            <li data-target="#myCarousel" data-slide-to="1"></li>
            <li data-target="#myCarousel" data-slide-to="2"></li>
        </ol>

        <!-- Wrapper for Slides -->
        <div class="carousel-inner">
            <div class="item active">
                <!-- Set the first background image using inline CSS below. -->
                <div class="fill" style="background-image:url('http://placehold.it/1900x1080&text=Tornado');"></div>
                <div class="carousel-caption">
                    <h2>Check out the <a href="http://www.tornadoweb.org/en/stable/">Tornado</a> project</h2>
                </div>
            </div>
            <div class="item">
                <!-- Set the second background image using inline CSS below. -->
                <div class="fill" style="background-image:url('http://placehold.it/1900x1080&text=Template');"></div>
                <div class="carousel-caption">
                    <h2>Tornado Templates are kind of a big thing</h2>
                </div>
            </div>
            <div class="item">
                <!-- Set the third background image using inline CSS below. -->
                <div class="fill" style="background-image:url('http://placehold.it/1900x1080&text=Server');"></div>
                <div class="carousel-caption">
                    <h2>Self serving!</h2>
                </div>
            </div>
        </div>

        <!-- Controls -->
        <a class="left carousel-control" href="#myCarousel" data-slide="prev">
            <span class="icon-prev"></span>
        </a>
        <a class="right carousel-control" href="#myCarousel" data-slide="next">
            <span class="icon-next"></span>
        </a>

    </header>

    <!-- Page Content -->
    <div class="container">

        <div class="row">
            <div class="col-lg-12">
                <h1>Tornado Template Server</h1>
                <p>This is a very simple bit of machinery to rapidly work on templates without the hassle of setting up the backend services</p>
            </div>
        </div>

        <hr>

    </div>
    <!-- /.container -->

        <script src="//cdnjs.cloudflare.com/ajax/libs/jquery/1.11.0/jquery.js"></script>
        <script src="//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.2.0/js/bootstrap.min.js"></script>
        
        <script>
            //<![CDATA[

            $(document).ready(function() {
                $('.carousel.slide').carousel({
                    interval: 5000
                });
            });

            //]]>
        </script>

    </body>
    
</html>

