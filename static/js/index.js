import {
    add_column,
    save_data,
    create_schema,
    select_fields,
    data_req,
    edit_req,
    gen_data,
    col_count,

} from "./functions.js";
import {schema_user, column_user} from "./jsDB.js";


if (document.location.pathname === '/creating_schema'){
    document.querySelector("#add_col").addEventListener("click", add_column);
    document.querySelector("#save_btn").addEventListener("click", create_schema);
    add_column();
}

if (document.querySelector("#save_btn") && document.location.pathname !== '/creating_schema'){
    document.querySelector("#add_col").addEventListener("click", add_column);
    col_count()
}

if (document.querySelector('#edit_template')) {
    const id = document.querySelector('#schema_id').innerText.slice(1);
    data_req(id)
    select_fields()
    document.querySelector("#save_btn").addEventListener("click", save_data);
    schema_user.id = Number(id)
    document.querySelector("#save_btn").addEventListener("click", edit_req);
}

if (document.querySelector("#gen_data")){
    document.querySelector("#gen_data").addEventListener("click", gen_data);
    console.log("done")

}
