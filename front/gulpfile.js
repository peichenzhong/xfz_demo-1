var gulp = require("gulp");
var cssnano = require("gulp-cssnano");
var rename = require("gulp-rename");
var uglify = require("gulp-uglify");
var concat = require("gulp-concat");
var cache = require("gulp-cache");
var imagemin = require("gulp-imagemin");
var bs = require("browser-sync").create();
var sass = require("gulp-sass");
var util = require("gulp-util");

// util 有一个方法log，可以打印js中的错误
var sourcemaps = require("gulp-sourcemaps");
//找出压缩css 之前的错误在哪里
var path = {
	'html':"./templates/**/",//**就是不管有多少层目录
	'css':"./src/css/**/",
	'js':"./src/js/",
	'images':"./src/images",
	'css_dist':"./dist/css/",
	'js_dist':"./dist/js/",
	'images_dist':"./dist/images/",

}

//定义一个html任务
gulp.task("html" , function () {
	// body...
	gulp.src(path.html+"*.html")
	.pipe(bs.stream())
});


gulp.task("greet",function () {
	// body...
	console.log("hello world");
});
//定义一个css任务
gulp.task("css" , function () {
	// body...
	gulp.src(path.css+"*.scss")
	.pipe(sass().on("error",sass.logError))
	.pipe(cssnano())
	.pipe(rename({"suffix":".min"}))
	.pipe(gulp.dest(path.css_dist))
	.pipe(bs.stream())
});
//定义一个js任务
gulp.task("js",function () {
	// body...
	console.log(path.js)
	console.log((path.js_dist))
	gulp.src(path.js+"*.js")
		.pipe(sourcemaps.init())
	//pipe(concat("index.js"))
	.pipe(uglify().on("erro",util.log))/*{"toplevel":true}*/
	.pipe(rename({"suffix":".min"}))
		.pipe(sourcemaps.write())
	.pipe(gulp.dest(path.js_dist))
	.pipe(bs.stream())
});



//定义一个图片压缩任务
gulp.task("images",function () {
	// body...
	gulp.src(path.images+"*.*")
	.pipe(cache(imagemin()))
	.pipe(gulp.dest(path.images_dist))
	.pipe(bs.stream())
});
//定义一个监听任务
gulp.task("watch",function () {
	// body...
	gulp.watch(path.css+"*.scss",['css'])
	gulp.watch(path.js +"*.js",["js"])
	gulp.watch(path.images +"*.*",["images"])
	gulp.watch(path.html +"*.html",["html"])
});

gulp.task("bs",function () {
	// body...
	bs.init({
		"server":
		{
			"baseDir":"./"
		}
	})
})


gulp.task("server",["watch"])