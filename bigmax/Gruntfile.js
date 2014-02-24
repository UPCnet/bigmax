module.exports = function(grunt) {
  // Configure
  grunt.initConfig({
    // The less task.
    less: {
      // This is the target's name "production".
      // You can run this task like this:
      //   grunt less:production
      production: {
        options: {
          // Set the option to compress the resulting css.
          yuicompress: false
        },
        files: {
          // Create a file called "public/css/site.css" from "less/site.less".
          // Note: If the directory public/css does not exist, it will be
          // created by the task.
          "stylesheets/bigmax.css": "less/bigmax.less"
        }
      }
    },

    watch: {
      // Keep an eye on those stylesheets.
      styles: {
        // The path 'less/**/*.less' will expand to match every less file in
        // the less directory.
        files: [ 'less/*.less'],
        // The tasks to run
        tasks: [ 'less' ]
      }
    }

  });

  // Load tasks
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-watch');

};
