local players = game:GetService('Players')
local http = game:GetService('HttpService')
local url = '{URL}/api/game/ban/check/' -- PUT YOUR URL IN THE {URL}

local headers = {
	['Content-Type'] = 'application/json',
	['authorization'] = 'PUT AUTHKEY HERE FROM .env' -- PUT YOUR AUTH KEY FROM .env HERE TO ACCESS SERVER
}

while task.wait(1) do
	for i, v in ipairs(players:GetPlayers()) do
		local data = http:RequestAsync({
			Url = url .. v.UserId,
			Method = 'GET',
			Headers = headers
		})
		local res = http:JSONDecode(data.Body)

		if res.code == 1 then
			v:Kick('you have been banned')
		elseif res.code == 0 then
			break
		else
			print('An error occurred.')
		end
	end
end
