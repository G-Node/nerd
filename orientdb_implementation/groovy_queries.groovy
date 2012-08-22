def my_query(pro, val) {
	def fun(sec) {
		def tmp = []
		sec['properties_coll'].each { i -> 
			println i.getClass()
			tmp.add(i.get('name') == 'TestedPro') }
		return tmp.contains(true)
	}
	
	println "---"
	def x = g.V.filter {fun(it)}
	return x
}