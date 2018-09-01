
$(document).ready(function() {
       $('#files').bind('change', handleFileSelect);
});


function handleFileSelect(evt) {
	var files = evt.target.files; // FileList object
	var file = files[0];
	// read the file metadata
	var output = ''
		output += ' - FileName:' + escape(file.name) + '<br />\n';
		output += ' - FileType: ' + (file.type || 'n/a') + '<br />\n';
		output += ' - FileSize: ' + file.size + ' bytes<br />\n';

	// read the file contents
	printTable(file);
	// post the results
	$('#list').append(output);
}
function printTable(file) {
	var reader = new FileReader();
	reader.readAsText(file);
	reader.onload = function(event){
		var csv = event.target.result;
		var data = $.csv.toArrays(csv);
		var html = '<thead> <tr>'+ 
					'<th scope="col">DOI</th>'+
					'<th scope="col">Category</th>'+
					'<th scope="col">Keywords</th>'+
					'</tr> </thead>\r\n'
		for(var row in data) {
			html += '<tr class="TableRows">\r\n';
			for(var item in data[row]) {
				html += '<td>' + data[row][item] + '</td>\r\n';
			}
			html += '</tr>\r\n';
		}
		$('#contents').html(html);
	};
	reader.onerror = function(){ alert('Unable to read ' + file.fileName); };
}

var allRows = document.getElementsByClassName("TableRows")
var filterInput = document.getElementById('filter-inputbox')
var filterButton = document.getElementById("filter-button")
var removeFilter = document.getElementById("clear-filter") 

filterButton.addEventListener("click",function(){ 
	filterResultsFromTable(filterInput.value)
	removeFilter.style.display = 'block';
 });

removeFilter.addEventListener("click",function(){ 
	removeFilter.style.display = 'none';
	filterInput.value = ""
	$.each(allRows,function (index,element) {
		element.style.display = 'table-row'
	});
 });


filterInput.addEventListener("keyup",function(){ 
	if (filterInput.value == "") {
		removeFilter.style.display = 'none';
		$.each(allRows,function (index,element) {
			element.style.display = 'table-row'
		});
	}
	else {
		removeFilter.style.display = 'block';
	}
});
function filterResultsFromTable(filterInput) {
	$.each(allRows,function (index,element) {
			var TdCellContent = element.querySelector("td:nth-child(3)").innerHTML
			if (TdCellContent.toLowerCase().indexOf(filterInput.toLowerCase()) > -1) {
			}
			else{
				element.style.display = 'none';
			}
	});
}
