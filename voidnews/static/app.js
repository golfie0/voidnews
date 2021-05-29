function Boxes(){
 const params = new URLSearchParams(window.location.search)
  var habrCheck = document.getElementById('habr')
  var tprogerCheck = document.getElementById('tproger')
  var dnewsCheck = document.getElementById('dnews')

  switch (params.get('habr')){
        case 0: habrCheck.checked = true;
        case 1: habrCheck.checked = false;
  }
    switch (params.get('tproger')){
        case 0: tprogerCheck.checked = true;
        case 1: tprogerCheck.checked = false;
  }
    switch (params.get('dnews')){
        case 0: dnewsCheck.checked = true;
        case 1: dnewsCheck.checked = false;
  }
}