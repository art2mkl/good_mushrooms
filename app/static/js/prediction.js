let choose_model = document.querySelector('.choose_model')
const loc_origin = window.location.origin

//-------------------------------------------------------------------------------------------------------------
//-----------------------------------------    FUNCTIONS     --------------------------------------------------
//-------------------------------------------------------------------------------------------------------------

function get_models() {
    //--------------------------------------------------------------------------------------------------------------
    //Select Models in current project
    //--------------------------------------------------------------------------------------------------------------         
        fetch(`${loc_origin}/prediction/choosemodel/`).then( response => {
            response.json().then( data => {
                
                let optionHTML = '';
                
                for (let model of data.models) {
                    optionHTML += '<option value="'+ model.id + '">' + `${model.name} accuracy : ${model.accuracy.toFixed(2)}, precision : ${model.precision.toFixed(2)}` + '</option>';
                }
                choose_model.innerHTML = optionHTML;                      
            });
        });
    }
get_models()