function map(property, value) {
	var i = this._id;
	var id = this.object_id;

	if (this.isLatest == true) {
		this.properties.forEach(
			function(z) { 
				if (z.name == property) {
					var checkValue = false;
					z.values.forEach(x)  {
						function(x) {
							if (x.value == value) {
								checkValue = true;
							}
						}
					}
	
					if (checkValue) {
						emit(i, id);
					}
				} 
			} 
		);
	}
}

function reduce(key, value) {
	return value;
}