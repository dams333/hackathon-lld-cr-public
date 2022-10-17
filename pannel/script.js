function open_details_overlay(id) {
    fetch('http://localhost:3000',)
    .then(function(response) {
        return response.json();
    }).then(function(data) {
        for (const dept in data) {
            for (const obj_dev of data[dept]) {
                const obj = obj_dev.data;
                if(obj.rna == id || obj.name == id) {
                    var overlay = document.getElementById('details-overlay');
                    overlay.style.display = 'block';
                    var overlay_title = document.getElementById('details-title');
                    var overlay_description = document.getElementById('details-description');
                    overlay_title.innerHTML = "";
                    overlay_description.innerHTML = "";
                    if(obj.data_type == "add") {
                        overlay_title.innerHTML = "New Association !<br>" + obj.data.name;
                        for (const key in obj.data) {
                            overlay_description.innerHTML += "- " + key + ": " + obj.data[key] + "<br>";
                        }
                    }
                    else if(obj.data_type == "update") {
                        overlay_title.innerHTML = "Update Association !<br>" + obj.original_obj.name;
                        if(obj.email != undefined)
                            overlay_description.innerHTML += "- New email: " + obj.email + "<br>";
                        if(obj.phone != undefined)
                            overlay_description.innerHTML += "- New phone: " + obj.phone + "<br>";
                        if(obj.address != undefined)
                            overlay_description.innerHTML += "- New address: " + obj.address + "<br>";
                    }
                    else if(obj.data_type == "problem") {
                        overlay_title.innerHTML = "Problem !<br>" + obj.name;
                        if(obj.rna.length > 0){
                            overlay_description.innerHTML += "The following RNA were found for the associations:<br>";
                            for (const key in obj.rna) {
                                overlay_description.innerHTML += "- " + obj.rna[key] + "<br>";
                            }
                        }
                        else {
                            overlay_description.innerHTML += "No RNA found for the associations.<br>";
                        }
                    }
                }
            }
        }
    });
}

function close_details_overlay() {
    var overlay = document.getElementById('details-overlay');
    overlay.style.display = 'none';
}

function accept_item(obj) {
    console.log("Register modification in database...")
    remove_from_db(obj);
}

function remove_from_db(id) {
    $.ajax({
        url : 'http://localhost:3000/delete/' + id,
        method : 'delete'
    })
    .done(function(data) {
        loadHTML();
    });
}


function open_rna_overlay(name) {
    var overlay = document.getElementById('rna-overlay');
    overlay.style.display = 'block';
    var overlay_title = document.getElementById('rna-title');
    overlay_title.innerHTML = "";
    overlay_title.innerHTML = "Select RNA code for " + name;
}

function close_rna_overlay() {
    var overlay = document.getElementById('rna-overlay');
    overlay.style.display = 'none';
}

function submit_rna(obj) {
    var rna = document.getElementById('rna-input').value;
    close_rna_overlay();
}

function loadHTML() {
    fetch('http://localhost:3000',)
    .then(function(response) {
        return response.json();
    }).then(function(data) {
        var div =  document.getElementById("content");
        div.innerHTML = "";
        for (const dept in data) {
            for (const obj of data[dept]) {
                const real_obj = obj.data;
                if(real_obj.data_type == 'add') {
                    div.innerHTML += `<div class="asso-component asso-add"><h2 class="asso-name">${real_obj.data.name}</h2><div class="btns"><button class="button button-detail" onclick="open_details_overlay('${real_obj.rna}')">View details</button><button class="button button-accept" onclick="accept_item('${real_obj.rna}')">Accept</button><button class="button button-deny" onclick="remove_from_db('${real_obj.rna}')">Deny</button></div></div>`;
                }
                if(real_obj.data_type == 'update') {
                    div.innerHTML += `<div class="asso-component asso-edit"><h2 class="asso-name">${real_obj.original_obj.name}</h2><div class="btns"><button class="button button-detail" onclick="open_details_overlay('${real_obj.rna}')">View details</button><button class="button button-accept" onclick="accept_item('${real_obj.rna}')">Accept</button><button class="button button-deny" onclick="remove_from_db('${real_obj.rna}')">Deny</button></div></div>`;
                }
                if(real_obj.data_type == 'remove') {
                    div.innerHTML += `<div class="asso-component asso-remove"><h2 class="asso-name">${real_obj.data.name}</h2><div class="btns"><button class="button button-accept" onclick="accept_item('${real_obj.rna}')">Accept</button><button class="button button-deny" onclick="remove_from_db('${real_obj.rna}')">Deny</button></div></div>`;
                }
                if(real_obj.data_type == 'problem') {
                    div.innerHTML += `<div class="asso-component asso-problem"><h2 class="asso-name">${real_obj.name}</h2><div class="btns"><button class="button button-detail" onclick="open_details_overlay('${real_obj.rna}')">View details</button><button class="button button-accept" onclick="open_rna_overlay('${real_obj.name}')">Choose RNA</button><button class="button button-deny" onclick="remove_from_db('${real_obj.name}')">Valid</button><button class="button button-deny" onclick="remove_from_db('${real_obj.name}')">Deny</button></div></div>`;
                }
            }
        }
    });
}