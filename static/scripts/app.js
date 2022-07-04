document.getElementById('movie-synopsis').innerHTML = movie_context[0];
document.getElementById('movie-synopsis').style.width = '100vw';
document.getElementById('movie-synopsis').style.marginLeft = '-5vw';

document.getElementById('serie-synopsis').innerHTML = serie_context[0];
document.getElementById('serie-synopsis').style.width = '100vw';
document.getElementById('serie-synopsis').style.marginLeft = '-5vw';

var a = document.getElementById('active');

var navb = document.getElementById('navb');
window.onscroll = function () { 
    "use strict";
    if (document.html.scrollTop >= 200 ) {
        navb.classList.add("black-nav");
        navb.classList.remove("bg-transparent");
    } 
    else {
        navb.classList.add("bg-transparent");
        navb.classList.remove("black-nav");
    }
};

function playVideo(srcVideo, vidSec){
    switch(vidSec) {
        case 1:
            video = document.getElementById('video1');
            break;
        case 2:
            video = document.getElementById('video2');
            break;
        default:
            video = document.getElementById('video3');
    } 

    var source = document.createElement('source');

    video.pause();
    video.src = srcVideo;
    source.src = srcVideo;
    video.load();
    video.play();
}

function stopVideo() { 
    document.getElementById('video').pause();
}

var carousel = document.querySelector('.carousel');
var flkty = new Flickity(document.getElementById('carousel1'), {
    cellAlign: 'left', autoPlay: 10000, pauseAutoPlayOnHover: true, initialIndex: 0
});

// Click Listener
flkty.on( 'staticClick', function( event, pointer, cellElement, cellIndex ) {
    if ( !cellElement ) {
        return;
    }

    var prevClickedCell = carousel.querySelector('.is-clicked');
    if ( prevClickedCell ) {
        prevClickedCell.classList.remove('is-clicked');
    } 
    var prevSelected = carousel.querySelector('.is-selected')
    if ( prevSelected ) { //If no cell was clicked, cell was prev auto selected. Remove selection.
        prevSelected.classList.remove('is-selected');
    }

    if( cellElement == prevClickedCell ) {
        //window.location = './sources/details/' + cellIndex + '.html';
        window.location = './home';
        return;
    }

    cellElement.classList.add('is-clicked');
    document.getElementById('movie-synopsis').innerHTML = movie_context[cellIndex];
    document.getElementById('movie-synopsis').style.width = '100vw';
    document.getElementById('movie-synopsis').style.marginLeft = '-5vw';

    playVideo(movie_trailers[cellIndex], 1);
});

// Selected Listener
flkty.on( 'select', function( index ) {
    //Detect if a cell was previously clicked. 
    var cellWasClicked = carousel.querySelector('.is-clicked');
    if ( cellWasClicked ) {
        return;
    }
    document.getElementById('movie-synopsis').innerHTML = movie_context[index];
    document.getElementById('movie-synopsis').style.width = '100vw';
    document.getElementById('movie-synopsis').style.marginLeft = '-5vw';

    playVideo(movie_trailers[index], 1);
});

var flkty2 = new Flickity(document.getElementById('carousel2'), {
    autoPlay: 10000, wrapAround: true, pauseAutoPlayOnHover: false
});

// Selected Listener
flkty2.on( 'select', function( index ) {
    document.getElementById('serie-synopsis').innerHTML = serie_context[index];
    document.getElementById('serie-synopsis').style.width = '100vw';
    document.getElementById('serie-synopsis').style.marginLeft = '-5vw';
    playVideo(serie_trailers[index], 2);
});

// Click Listener
flkty2.on( 'staticClick', function( event, pointer, cellElement, cellIndex ) {
    if ( typeof cellIndex == 'number' ) {
        if( cellIndex == flkty2.selectedIndex ) {
            window.location = './home';
            return;
        }
        flkty2.selectCell( cellIndex );
    }
    document.getElementById('serie-synopsis').innerHTML = serie_context[cellIndex];
    document.getElementById('serie-synopsis').style.width = '100vw';
    document.getElementById('serie-synopsis').style.marginLeft = '-5vw';
    

    playVideo(serie_trailers[cellIndex], 2);
});
