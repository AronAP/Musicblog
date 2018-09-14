var
  gulp            = require("gulp"),
  browserSync     = require('browser-sync'),
  sass            = require("gulp-sass"),
  autoprefixer    = require("gulp-autoprefixer"),
  cleancss        = require("gulp-clean-css"),
  concatCss       = require('gulp-concat-css'),
  rename          = require("gulp-rename"),
  ftp             = require("gulp-ftp"),
  gutil           = require('gulp-util');


gulp.task('browser-sync', function() {
    browserSync({
        server: {
            baseDir: 'src'
        },
        notify: false
    });
});

gulp.task("reload-css", function() {
  gulp.src('./src/sass/**/*.scss')
    .pipe(sass().on('error', sass.logError))
    .pipe(autoprefixer({
      browsers: ['last 3 version'],
      cascade: false
    }))
    .pipe(concatCss("style.css"))
    .pipe(gulp.dest('./src/css/'))
    .pipe(cleancss({
      compatibility: 'ie8'
    }))
    .pipe(rename({
      suffix: '.min'
    }))
    .pipe(gulp.dest('./src/css/'))
    .pipe(browserSync.reload({stream: true}))
});

gulp.task('ftp', function () {
  return gulp.src('dist/**')
    .pipe(ftp({
      host: 's2.hostiman.ru',
      user: 'artempry',
      pass: 'ib786Yb4Cw',
      remotePath: '/www/artemprydybailo.h1n.ru/work'
    }))
    .pipe(gutil.noop());
});

gulp.task('default', ['browser-sync', 'reload-css'], function() {
    gulp.watch('src/sass/**/*.scss', ['reload-css']);
    gulp.watch('src/**/*.html', browserSync.reload);
    gulp.watch('src/js/**/*.js', browserSync.reload);
});