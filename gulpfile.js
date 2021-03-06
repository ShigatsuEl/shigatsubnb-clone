const gulp = require("gulp");

const css = () => {
  const postCSS = require("gulp-postcss");
  const sass = require("gulp-sass");
  const minify = require("gulp-csso");
  sass.compiler = require("node-sass");
  // 기본적으로 assets/scss/styles.scss 파일을 sass를 통해 normal css로 변환할 것이다
  // postCSS에서 사용할 2개의 플러그인은 tailwindcss와 autoprefixer
  // 위 두개의 플러그인은 css코드에 있는 tailwindcss에서만 사용하는 @apply 등을 브라우저가 이해할 수 있는 css로 변환한다
  // 모든 것이 끝나면 minify를 통해 파일을 작게 만들어 static/css라는 장소에 결과물을 css로 보여줄 것이다
  return gulp
    .src("assets/scss/styles.scss")
    .pipe(sass().on("error", sass.logError))
    .pipe(postCSS([require("tailwindcss"), require("autoprefixer")]))
    .pipe(minify())
    .pipe(gulp.dest("static/css"));
};

exports.default = css;
