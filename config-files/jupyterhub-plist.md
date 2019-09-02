Save as `/Library/LaunchDaemons/local.jupyterhub.plist`:

```
<plist version="1.0">
<dict>
	<key>KeepAlive</key>
	<true/>

	<key>Label</key>
	<string>local.jupyterhub</string>

	<key>ProgramArguments</key>
	<array>
		<string>/bin/bash</string>
		<string>-c</string>
		<string>conda activate jupyter-env; jupyterhub --config=/etc/jupyterhub/jupyterhub_config.py</string>
	</array>
  
	<key>OnDemand</key>
	<true/> 

	<key>ServiceDescription</key>
	<string>JupyterHub Service</string>

	<key>WorkingDirectory</key>
	<string>/etc/jupyterhub</string>

	<key>StandardOutPath</key>
	<string>/var/log/jupyterhub.stdout</string>

	<key>StandardErrorPath</key>
	<string>/var/log/jupyterhub.stderr</string>

	<key>EnvironmentVariables</key>
	<dict>
		<key>PATH</key>
		<string>/Library/TeX/Distributions/.DefaultTeX/Contents/Programs/texbin:/anaconda3/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/X11/bin</string>
	</dict>

	<key>RunAtLoad</key>
	<true/>
</dict>
</plist>
```
