from web import app
import utils

app.secret_key = 'adlj;ja;dlk'

config = utils.get_config('web')
app.config.update(config)

if __name__ == '__main__':
    app.run(host=config.get('bind','0.0.0.0'),port=int(config.get('port')),debug=True)
