var gulp = require('gulp');
var less = require('gulp-less');
var concat = require('gulp-concat');
var sourcemaps = require('gulp-sourcemaps');
var minifyCSS = require('gulp-minify-css');
var minify = require('gulp-minify');
var uglify = require('gulp-uglify');

var paths = {
    less: './less/**/*.less',
    scripts: './js/**/*.js'
};

gulp.task('less', function () {
    return gulp.src(paths.less)
        .pipe(sourcemaps.init())
        .pipe(less())
        .pipe(minifyCSS())
        .pipe(sourcemaps.write())
        .pipe(concat('app.min.css'))
        .pipe(gulp.dest('./public_html/css'));
});

gulp.task('scripts', function () {
    return gulp.src(paths.scripts)
        .pipe(concat('app.min.js'))
        .pipe(uglify())
        .pipe(gulp.dest('./public_html/js'));
});

gulp.task('default', ['less', 'scripts']);

gulp.task('watch', function () {
    gulp.watch(paths.scripts, ['scripts']);
    gulp.watch(paths.less, ['less']);
});