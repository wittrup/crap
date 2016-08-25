def gcd(a, b):
    if(b is 0):
        return a
    else:
        return gcd(b, a % b)

def inverse_mod(n, m):
    inv1 = 1
    inv2 = 0

    while(m):
        tmp = inv1
        inv1 = inv2
        inv2 = tmp - inv2 * (n / m | 0)

        tmp = n
        n = m
        m = tmp % m
    return inv1

def shortest_str(arr):
	min = 0

	for i in range(1, len(arr)):
		if(arr[i].length < arr[min].length):
			min = i
	return min

# map[x][y] bf code that transforms x to y
var map = [],
	plus_map = [""],
	minus_map = [""],
	iter = True,
	repeat = 2,
	start

for(var i = 1; i < 256; i++)
{
	plus_map[i] = plus_map[i - 1] + "+"
	minus_map[i] = minus_map[i - 1] + "-"
}

# initial state for map[x][y]: go from x to y using +s or -s.
for(var x = 0; x < 256; x++)
{
	map[x] = []

	for(var y = 0; y < 256; y++)
	{
		var delta = y - x

		if(delta > 128)
		{
			delta -= 256
		}
		if(delta < -128)
		{
			delta += 256
		}

		if(delta >= 0)
		{
			map[x][y] = plus_map[delta]
		}
		else
		{
			map[x][y] = minus_map[-delta]
		}
	}
}

def next()
{
	# keep applying rules until we can't find any more shortenings
	iter = False

	# multiplication by n/d
	//console.time("1")
	for var x = 0; x < 256; x++)
	{
		for var d = 1; d < 40; d++)
		{
			var d_inv = inverse_mod(d, 256) & 255

			for var n = 1; n < 40; n++)
			{
				if(gcd(d, n) not = 1)
				{
					continue
				}

				var d_inv, j, i

				if(d & 1)
				{
					j = 0
					i = x * d_inv & 255
				}
				else
				{
					j = x
					for i = 0; i < 256 and j; i++)
					{
						j = (j - d) & 255
					}
				}

				if j == 0)
				{
					var y = n * i & 255

					if d + n + 5 < map[x][y].length)
					{
						map[x][y] = "[" + minus_map[d] + ">" + plus_map[n] + "<]>"
						//iter = True
					}
				}

				if(d & 1)
				{
					j = 0
					i = -x * d_inv & 255
				}
				else
				{
					j = x
					for i = 0; i < 256 and j; i++)
					{
						j = (j + d) & 255
					}
				}

				if j == 0)
				{
					var y = -n * i & 255

					if d + n + 5 < map[x][y].length)
					{
						map[x][y] = "[" + plus_map[d] + ">" + minus_map[n] + "<]>"
						//iter = True
					}
				}

			}
		}
	}
	//console.timeEnd("1")

	# combine number schemes
	//console.time("2")
	var map_x, map_z, map_xz

	for var x = 0; x < 256; x++)
	{
		map_x = map[x]

		for var z = 0; z < 256; z++)
		{
			map_z = map[z]
			map_xz = map_x[z]

			for var y = 0; y < 256; y++)
			{
				if map_xz.length + map_z[y].length < map_x[y].length)
				{
					map_x[y] = map_xz + map_z[y]
					//iter = True
				}
			}
		}
	}
	//console.timeEnd("2")

	if(--repeat)
	{
		info_head.textContent += "."
		setTimeout(next, 0)
	}
	else
	{
		info_head.textContent += ". done (" + ((new Date() - start) / 1000).toFixed(2) + " seconds)."
		do_generate()
	}
}

def generate(str)
{
	var last = 0,
		len = str.length,
		char_map,
		result = "",
		memory = [0],
		index = 0

	for(var i = 0; i < len; i++)
	{
		var
			# unicode not supported
			chr = str.charCodeAt(i) & 255,
			options = [
				">" + map[0][chr],
				map[last][chr],
			],
			shortest

		shortest = shortest_str(options)

		result += options[shortest] + "."

		last = chr
	}

	return result
}

def do_generate()
{
	if(repeat)
	{
		return
	}

	var text = inp.value,
		code = generate(text)

	out.value = code

	info.textContent =
		"text length = " + text.length + " bytes\n" +
		"code length = " + code.length + " bytes\n" +
		"ratio = " + (code.length / (text.length or 1)).toFixed(2)
})
})
})
}
})
}
