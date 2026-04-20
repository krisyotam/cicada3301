import * as path from 'path'
import {main} from './core/main'

export const DataPath = path.join(__dirname, '../', 'data')
export const OutputPath = path.join(__dirname, '../', 'data', 'output')
export const TasksFile = 'tasks.txt'

main()