var gulp = require('gulp');
var less = require('gulp-less');
var minifyCSS = require('gulp-csso');
var browserSync = require('browser-sync').create();

gulp.task('serve', ['less', 'js'], function() {
    browserSync.init({
		proxy: "localhost:4567",
		open: false,
		ui: false
    });

    gulp.watch("less/*.less", ['less']).on('change', browserSync.reload);
    gulp.watch("js/*.js", ['js']).on('change', browserSync.reload);
    gulp.watch("templates/*.html").on('change', browserSync.reload);
});

gulp.task('less', function() {
  return gulp.src('less/*.less')
    .pipe(less())
    .pipe(minifyCSS())
    .pipe(gulp.dest('static/dist/css'))
});

gulp.task('js', function () {
  return gulp.src('js/*js')
    .pipe(gulp.dest('static/dist/js'));
});

gulp.task('default', [ 'less', 'js', 'serve' ]);