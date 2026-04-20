import * as os from 'os'

export const LogFile = 'LiberPrimusSolver.log'
import * as fs from 'fs'

export class Logger {
    constructor() {
        if (!!Logger.instance) {
            return Logger.instance
        }

        Logger.instance = this
        fs.writeFileSync(LogFile, '')

        this.fileStream = fs.createWriteStream(LogFile, {flags: 'a'})

        return this
    }

    log = (module, message) => {
        const date = new Date()
        const timestamp = `${date.getDay()}/${date.getMonth()}/${date.getFullYear()} ${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}.${date.getMilliseconds()}`
        const log = `${timestamp} - ${module}: ${message}`

        console.log(log)

        this.fileStream.write(log + os.EOL)
    }
}