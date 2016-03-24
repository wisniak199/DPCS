var gulp = require('gulp');
var less = require('gulp-less');
var concat = require('gulp-concat');
var sourcemaps = require('gulp-sourcemaps');
var minifyCSS = require('gulp-minify-css');
var minify = require('gulp-minify');
var uglify = require('gulp-uglify');
var browserSync = require('browser-sync').create();


var paths = {
    less: './less/**/*.less',
    htmls: './public_html/*.html',
    scripts: [
        './js/libs/jquery.js', //jquery must be befeore bootstrap
        './js/**/*.js'
    ]
};

gulp.task('less', function () {
    return gulp.src(paths.less)
        .pipe(sourcemaps.init())
        .pipe(less())
        .pipe(minifyCSS())
        .pipe(sourcemaps.write())
        .pipe(concat('app.min.css'))
        .pipe(gulp.dest('./public_html/css'))
        .pipe(browserSync.stream());
});

gulp.task('scripts', function () {
    return gulp.src(paths.scripts)
        .pipe(concat('app.min.js'))
        .pipe(uglify())
        .pipe(gulp.dest('./public_html/js'));
});

gulp.task('default', ['less', 'scripts']);

gulp.task('watch', function () {

    browserSync.init({
        server: {
            baseDir: "./public_html"
        },
        startPath: "/index.html"
    });

    gulp.watch(paths.scripts, ['scripts'],browserSync.reload);
    gulp.watch(paths.htmls).on('change', browserSync.reload);
    gulp.watch(paths.less, ['less']);
});