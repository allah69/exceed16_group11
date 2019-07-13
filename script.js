const baseurl = "https://exceed.superposition.pknn.dev/data/pangpond"
//array
var time_array = new Array()
var category_array = new Array()
var task_array = new Array()




function handleClick() {
    var d = new Date()
    var current_hour = d.getHours()    
    if (current_hour > 23) {
        current_hour = current_hour - 24
    } 
    //item in array
    var time = document.getElementById("time1").value
    var category = document.getElementById("category").value
    var task = document.getElementById("name").value

    //add objects to array
    // time_array.push(time)
    // category_array.push(category)
    // task_array.push(task)

    fetch(baseurl)
    .then((res) => res.json())
    .then((data) => {
        console.log(data);
        let tmp_task = data["task"]
        let tmp_categ = data["category"]
        let tmp_time = data["time"]
        tmp_categ.push(category)
        tmp_task.push(task)
        tmp_time.push(time)

        console.log("click")
        fetch(baseurl,{
            method:"POST",
            body: JSON.stringify({
                "data" :{
                    "task" : tmp_task,                
                    "time" : tmp_time,
                    "category" : tmp_categ,
                    "current time" : current_hour
                }
            }),
            headers : {
                "Content-Type" : "application/json"
            }
        }).then((res) => res.json())
        .then((data) => {
            window.location = 'products.html';
            console.log(data)
        })
        .catch((err) => console.log(err));
        
})
return false;
}
