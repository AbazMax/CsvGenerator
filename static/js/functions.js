import {schema_user, column_user} from "./jsDB.js";
let count = 0

/**
 * Count columns on page during creation or editing schemas
 */
export function col_count(){
    console.log(count)
    let id_list = [];
    const [...columns] = document.querySelectorAll("#columns > .row");
    console.log(columns)
    for (let col of columns) {
        id_list.push(Number(col.id.slice(2)))
    }
    const max_id = (Math.max.apply(null, id_list))
    if (max_id > 0){
        count = max_id
    }
}

/**
 * Add a new column during creation or editing schemas
 */
export function add_column (){
    col_count()
    const col_list = document.querySelector("#columns");
    count++
    col_list.insertAdjacentHTML("beforeend", `
    <div class="row" id=\c_${count}\>
        <div class="col-4">
            <p>
                Column name<br>
                <input type="text" name="name" class="form-control">
            </p>
        </div>
        <div class="col-3">
            <p>
                Type<br>
                <select name="col_type" class="form-control" id=\s_${count}\ data-type="col_type">
                <option value="full_name">Full name</option>
                <option value="age">Age</option>
                <option value="phone_number">Phone number</option>
                <option value="address">Address</option>
                <option value="date">Date</option>
                <option value="job">Job</option>
                <option value="company">Company</option>
            </select>
            </p>
        </div>
        <div class="row col-2 invisible">
            <div class="col-6">
                Min<br>
                <input name="range-min" class="form-control" type="number">
            </div>
            <div class="col-6">
                Max<br>
                <input name="range-max" class="form-control" type="number">
            </div>
        </div>
        <div class="col-2">
            <p>
            Order<br>
            <input name="order" class="form-control" type="number">
            </p>
        </div>
        <div class="col-1">
        <div class="delete_col_btn" id=\d_${count}\ style="color: #D9534F">Delete</div>
        </div>
    </div>`);

    is_range()
    delete_cols()
}

/**
 * Add or hide range fields depends of data type
 */
export function is_range(){
    const [...types] = document.querySelectorAll("#columns > .row select");
    for (let sel of types){
        sel.onchange = (evt) => {
            const col_id = evt.target.id.slice(2);
            const range_field = document.querySelector(`#c_${col_id} > .row`);
            if (evt.target.value === "age"){
                range_field.classList.remove("invisible");
            }else{
                range_field.classList.add("invisible");
            }
        }
    }
}

/**
 * Delete columns during creation or editing schemas
 */
function delete_cols(){
    const [...del_btns] = document.querySelectorAll(".delete_col_btn")
    for (let btn of del_btns){
        btn.onclick = (evt) =>{
            const id = evt.target.id.slice(2);
            document.querySelector(`#c_${id}`).remove();
        }
    }
}

/**
 * Create columns and add them to schema object
 * @returns list of columns
 */
function col_creation(){
    const col_list = [];
    const [...columns] = document.querySelectorAll("#columns > .row");
    for (let column of columns){
        const new_col_obj = {
            col_name: "",
            col_type: "",
            range_min: "",
            range_max: "",
            order: "",
            c_id: "",
        }

        new_col_obj.c_id = column.id
        new_col_obj.col_type = column.querySelector("select").value;

        const [...inputs] = column.querySelectorAll("input");
        for (let inp of inputs){
            if (inp.name === "name"){
                new_col_obj.col_name = inp.value;
            }else if(inp.name === "range-min"){
                new_col_obj.range_min = inp.value;
            }else if(inp.name === "range-max"){
                new_col_obj.range_max = inp.value;
            }else if(inp.name === "order"){
                new_col_obj.order = inp.value;
            }
        }
        col_list.push(new_col_obj)
    }
    return col_list
}

/**
 * Create schema object to send it on server
 * @returns schema object
 */
export function save_data(){
    const inp_name = document.querySelector("#name");
    const inp_col_sep = document.querySelector("#col_sep");
    const inp_str_char = document.querySelector("#str_char");

    schema_user.name = inp_name.value
    schema_user.col_sep = inp_col_sep.value
    schema_user.str_char = inp_str_char.value
    schema_user.columns = col_creation()
    console.log(schema_user)
    return schema_user
}

/**
 * Request for creating schema instance
 */
export function create_schema(){
    const [...inputs] = document.querySelectorAll("input")
    for (let inp of inputs){
        if (inp.name !== 'range-min' && inp.name !== 'range-max' && inp.value === ''){
            alert('Please fill all fields');
            return
        }
    }
    fetch("save_schema", {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify(save_data())
    })
    .then(response => response.json())
    .then(data => {
        document.location = `data_sets/${data.id}`
    });
}

/**
 * Request data to edit schema
 * @param id
 */
export function data_req(id){
    fetch(`/data_req/${id}`, {
        method: 'GET',
        headers: {"X-Requested-With": "XMLHttpRequest",}
    })
    .then(response => response.json())
    .then(data => {
        choose_select(data)
    });
}


export function select_fields(){
    const id = document.querySelector('#schema_id').value;
    is_range()
    delete_cols()
}

/**
 * Choose selects and activate options
 * @param data
 */
function choose_select(data){
    console.log(data)
    const [...options] = document.querySelectorAll("option")
    for (let optn of options){
        if (optn.value === data.col_sep){
            optn.setAttribute("selected", true);
        }else if(optn.value === data.str_char){
            optn.setAttribute("selected", true);
        }
    }
    const [...selects] = document.querySelectorAll("select")
    for (let sel of selects){
        for (let col of data.columns){
            if(sel.id === col.user_id){
                for (let optn of sel.children){
                    if(optn.value === col.col_type){
                        optn.setAttribute("selected", true)
                    }
                }
            }else if(col.col_type == "age"){
                const range_field = document.querySelector(`#${col.user_id} > .row`);
                range_field.classList.remove("invisible");
                for (let inp of [...range_field.querySelectorAll("input")]){
                    if(inp.name === "range-min"){
                        inp.value = col.range_min;
                    }else if(inp.name === "range-max"){
                        inp.value = col.range_max;
                    }
                }
            }
        }
    }
}

/**
 * Request for save changed data
 */
export function edit_req(){
    const [...inputs] = document.querySelectorAll("input")
    for (let inp of inputs){
        if (inp.name !== 'range-min' && inp.name !== 'range-max' && inp.value === ''){
            alert('Please fill all fields');
            return
        }
    }
    fetch("/edit_req", {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify(schema_user)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        document.location = `/data_sets/${data.id}`

    });
}

/**
 * Request for generating csv file
 */
export function gen_data(){
    const id = document.querySelector("#sch_id").value;
    const rows = document.querySelector("#rows").value;
    const indicator = document.querySelector(`#s_${id} #indicator`);
    const link = document.querySelector(`#s_${id} a`);
    indicator.innerHTML = "Creating...";
    indicator.classList.add("creating")
    fetch("/gen_data", {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({'id': id, 'rows': rows})
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        indicator.classList.remove("creating");
        indicator.classList.remove("not_ready");
        indicator.classList.add("ready");
        indicator.innerHTML = "Ready";
        link.classList.remove("disabled");
    });
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

