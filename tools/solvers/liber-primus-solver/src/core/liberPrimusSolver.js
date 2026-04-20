import * as fs from 'fs'
import * as path from 'path'
import 'regenerator-runtime/runtime'
import {Logger} from '../utils/logger'
import {Atbash} from '../ciphers/atbash'
import {readFileLines, setupOutputFolder, writeFile} from '../utils/fileUtils'
import {Shift} from '../ciphers/shift'
import {Vigenere} from '../ciphers/vigenere'
import {LiberPrimusSplitter} from './liberPrimusSplitter'
import {DataPath, TasksFile} from '../app'
import {HillCipher} from '../ciphers/hillCipher'
import {DecryptTask} from './taskTypes/decryptTask'
import {PartitionsTask} from './taskTypes/partitionsTask'
import {ScanTotientTask} from './taskTypes/scanTotientTask'

export class LiberPrimusSolver {
    constructor() {
        this.logger = new Logger()
        this.atbash = new Atbash()
        this.shift = new Shift()
        this.tasksFile = path.join(DataPath, TasksFile)
        this.liberPrimusSplitter = new LiberPrimusSplitter()
    }

    fileData = fileName => fs.readFileSync(path.join(DataPath, fileName), 'utf-8')

    run = async () => {
        this.logger.log('LiberPrimusSolver', 'Liber Primus Solver started')

        setupOutputFolder()

        await this.performTasks()

        this.logger.log('LiberPrimusSolver', 'Liber Primus Solver stopped')
    }

    performTasks = async () => {

        for (const line of readFileLines(this.tasksFile)) {
            if (line.startsWith('//'))
                continue

            try {
                const taskConfiguration = JSON.parse(line)

                const {taskType} = taskConfiguration
                this.logger.log('LiberPrimusSolver', `Starting task. Type:${taskType}, data: ${line}`)

                if (taskType === 'decrypt') {
                    const decryptTask = new DecryptTask(this.fileData)
                    decryptTask.apply(taskConfiguration)
                } else if (taskType === 'partitions') {
                    const partitionsTask = new PartitionsTask()
                    partitionsTask.apply(taskConfiguration)
                } else if (taskType === 'scanTotient') {
                    const scanTotientTask = new ScanTotientTask()
                    scanTotientTask.apply(taskConfiguration)
                } else {
                    throw 'Unsupported or missing taskType'
                }

            } catch (e) {
                this.logger.log(e)
            }
        }
    }
}