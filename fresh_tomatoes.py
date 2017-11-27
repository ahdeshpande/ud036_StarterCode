import webbrowser
import os
import re

# Styles and scripting for the page
main_page_head = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Fresh Tomatoes!</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet"
    href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet"
    href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script
    src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js">
    </script>
    <style type="text/css" media="screen">
        body {
            padding-top: 80px;
            font-family: "Avenir", "Helvetica Neue", Arial, sans-serif;
        }

        #trailer .modal-dialog {
            width: 75%;
        }

        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }

        #trailer-video {
            width: 100%;
            height: 100%;
        }

        .movie-tile {
            margin-bottom: 20px;
            padding-top: 20px;
            position: relative;
            min-height: 500px;
        }

        .movie-tile:hover {
            background-color: #EEE;
            cursor: pointer;
        }

        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }

        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }

        .overlay {
            position: absolute;
            bottom: 100%;
            left: 0;
            right: 0;
            background-color: rgba(0, 0, 0, 0.75);
            overflow: hidden;
            width: 100%;
            height: 0;
            transition: .5s ease;
        }

        .movie-tile:hover .overlay {
            bottom: 25%;
            height: 75%;
        }

        .overview {
            text-align: left;
            font-size: 14px;
            white-space: normal;
            color: white;
            position: absolute;
            overflow: hidden;
            top: 25%;
            left: 33%;
            transform: translate(-25%, -25%);
            -ms-transform: translate(-25%, -25%);
        }
    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal',
        function (event) {
            // Remove the src so the player itself gets removed, as this is the
            // only reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.movie-tile', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId
             + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>",
            {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
    </script>
</head>
'''

# The main page layout and title bar
main_page_content = '''
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal"
          aria-hidden="true">
            <img src="https://tinyurl.com/ycbwohmh"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>

    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="navbar-brand" href="#">Fresh Tomatoes Movie Trailers</a>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
        <div class="row">
            {movie_tiles}
        </div>
    </div>
    <p class="text-center">
    This product uses the TMDb API but is not endorsed or certified by TMDb.
    <br>
    <a href="https://www.themoviedb.org/" target="_blank">
        <img src="https://tinyurl.com/ybvuqwra" style="max-height: 30px;">
    </a>
    </p>
  </body>
</html>
'''

# A single movie entry html template
movie_tile_content = '''
<div class="col-md-6 col-lg-4 movie-tile text-center"
data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal"
data-target="#trailer">
    <img src="{poster_image_url}" width="220" height="342">
    <h3>{movie_title} ({release_year})</h3>
    <h4>Rating: {rating}</h4>
    <div class="overlay">
        <div class="overview">{overview}</div>
    </div>
</div>
'''


def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(
            r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(
            r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
        trailer_youtube_id = (youtube_id_match.group(0) if youtube_id_match
                              else None)

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title=movie.title,
            overview=movie.storyline,
            poster_image_url=movie.poster_image_url,
            trailer_youtube_id=trailer_youtube_id,
            release_year=movie.release_year,
            rating=movie.rating,
        )
    return content


def open_movies_page(movies):
    # Create or overwrite the output file
    output_file = open('fresh_tomatoes.html', 'w')

    # Replace the movie tiles placeholder generated content
    rendered_content = main_page_content.format(
        movie_tiles=create_movie_tiles_content(movies))

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser (in a new tab, if possible)
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2)
