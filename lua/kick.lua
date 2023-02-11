local players = game:GetService('Players')
local http = game:GetService('HttpService')
local url = '{URL}/api/game/kick/check/'

while task.wait(0) do
	for i, v in ipairs(players:GetPlayers()) do
		local data = http:GetAsync(url .. v.UserId)
		local res = http:JSONDecode(data)

		if res.code == 1 then
			v:Kick('kicked website')
		elseif res.code == 0 then
			break
		else
			print('An error occured.')
		end
	end
end