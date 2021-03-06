<!DOCTYPE html>

<html lang="en">

  <head>  
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">

    <!-- Meta Data -->
    <meta name="viewport" content="width=device-width">
    <meta name="description" content="Daily Automated Report">
    <meta name="author" content="Daniel Goldmith <djgoldsmith@googlemail.com>">
  </head>

  <body>
    <h1>${project}: Daily cogent-house report ${date.date()}</h1>

    <h2 id="sec-1">Server and house overview</h2>
    <div class="outline-text-2" id="text-1">
      <table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


	<colgroup>
	  <col  class="left" />
	  <col  class="right" />
	</colgroup>
	<thead>
	  <tr>
	    <th scope="col" class="left">&#xa0;</th>
	    <th scope="col" class="right">Number</th>
	  </tr>
	</thead>
	<tbody>
	  <tr>
	    <td class="left">Total servers deployed</td>
	    <td class="right">${deployed_serv}</td>

	  </tr>

	  <tr>
	    <td class="left">Number of houses</td>
	    <td class="right">${deployed_houses}</td>
	  </tr>

	  <tr>
	    <td class="left">Total number of nodes deployed</td>
	    <td class="right">${deployed_nodes}</td>
	  </tr>

	  <tr>
	    <td class="left">Servers that have pushed today</td>
	    <td class="right">${push_today}</td>
	  </tr>
	</tbody>
      </table>
    </div>
</div>

<div id="outline-container-sec-2" class="outline-2">
  <h2 id="sec-2">Push / server status</h2>
  <div class="outline-text-2" id="text-2">
    <table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


      <colgroup>
	<col  class="left" />

	<col  class="right" />

	<col  class="right" />
      </colgroup>
      <thead>
	<tr>
	  <th scope="col" class="left">&#xa0;</th>
	  <th scope="col" class="right">Number</th>
	  <th scope="col" class="right">Percentage</th>
	</tr>
      </thead>
      <tbody>
	<tr>
	  <td class="left">Deployed servers that have pushed this week</td>
	  <td class="right">${push_week}</td>
	  <td class="right">${"{0:.2f}".format(float(push_week) / (float(deployed_serv)) * 100)}%</td>
	</tr>

	<tr>
	  <td class="left">Deployed servers that have pushed today</td>
	  <td class="right">${push_today}</td>
	  <td class="right">${"{0:.2f}".format((float(push_today) / deployed_serv) * 100)}%</td>
	</tr>
	<tr>
	  <td class="left">Houses with data in the past 24 hours</td>
	  <td class="right">${houses_today}</td>
	  <td class="right">${"{0:.2f}".format((float(houses_today) / deployed_houses) * 100)}%</td>
	</tr>
      </tbody>
    </table>
  </div>
</div>

<div id="outline-container-sec-4" class="outline-2">
  <h2 id="sec-4">Node status</h2>
  <div class="outline-text-2" id="text-4">
    <table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">

      <colgroup>
	<col  class="left" />

	<col  class="right" />

	<col  class="right" />
      </colgroup>
      <thead>
	<tr>
	  <th scope="col" class="left">&#xa0;</th>
	  <th scope="col" class="right">Number</th>
	  <th scope="col" class="right">Percentage</th>
	</tr>
      </thead>
      <tbody>
	<tr>
	  <td class="left">Total nodes in last week</td>
	  <td class="right">${node_week}</td>
	  <td class="right">${"{0:.2f}".format((float(node_week) / deployed_nodes) * 100)}%</td>
	</tr>

	<tr>
	  <td class="left">Total nodes in last 24 hours</td>
	  <td class="right">${node_today}</td>
	  <td class="right">${"{0:.2f}".format((float(node_today) / deployed_nodes) * 100)}%</td>
	</tr>


      </tbody>
    </table>

  </div>
</div>


<div id="outline-container-sec-3" class="outline-2">
  <h2 id="sec-3">Houses with partial data (did not report in the last 8 hours):</h2>
  <ul>
    	%for house in houses_partial:
	  <li>${house[0]}</li>
	  <ul>	 
          %for node in house[1]:
	      <li>Missing: ${node}</li>
          %endfor
          </ul>
	%endfor
  </ul>
</div>

<div id="outline-container-sec-3" class="outline-2">
  <h2 id="sec-3">Houses with no data:</h2>
  <ul>
    	%for house in houses_missing:
	  <li>${house[0]}</li>
	  <ul>	 
          %for node in house[1]:
	      <li>Missing: ${node}</li>
          %endfor
          </ul>
	%endfor
  </ul>
</div>


<div id="outline-container-sec-6" class="outline-2">
  <h2 id="sec-5">These nodes have a battery voltage less than the
  minimum recommended:</h2>
  <div class="outline-text-2" id="text-5">
    <ul>
      %for node in battery_warnings:
      <li>${node}</li>
      %endfor
    </ul>
  </div>
</div>

<div id="outline-container-sec-5" class="outline-2">
  <h2 id="sec-5">Pulse nodes where the value has not changed in the past day</h2>
  <div class="outline-text-2" id="text-5">
    <ul>
      %for node in pulse_warnings:
      <li>${node}</li>
      %endfor
    </ul>
  </div>
</div>

</body>

</html>
