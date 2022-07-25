// for dates
// $('.datepicker').datepicker({
//     inline: true
// });



// $('.datepicker').datepicker();


// ! Get today's date
// var today = new Date();
// var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
// var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
// var dateTime = date+' '+time;

// function getDate() {
    // console.log(date);
//     return date;
// }


// ! prefill date id with current date
(function () {
    var date = new Date().toISOString().substring(0, 10),
        field = document.querySelector('#date');
    field.value = date;
    // console.log(field.value);
})()


// ! change the date automcatically by an hour
function changeEndTime() {


    start_time = document.querySelector('#start_time');
    end_time = document.querySelector('#end_time');

    if (end_time.value) {return;} // do notthing if already changed

    start_time_obj = new Date("2000-01-01 " + start_time.value);
    // add one hour and convert to string, in a correct format
    end_time_obj_str = new Date(start_time_obj.getTime() + (3600 * 1000)).toTimeString().substring(0, 8); 
    end_time.value = end_time_obj_str;

    // console.log(new Date(start_time_obj.getTime() + (3600 * 1000)).toTimeString());

    // if you want to chate to today's date
    // var now = new Date();
    // var nowDateTime = now.toISOString();
    // var nowDate = nowDateTime.split('T')[0];
    // var hms = '01:12:33';
    // var target = new Date(nowDate + hms);
    // console.log(target);
    

    // TODO maybe set the end time to empty and chage only if changed
}