import './App.css';
import TodoList from './components/Todos';

function App() {
  return (
    <div className='App'>
      <header className='App-header'>
        <h1>Todo Management App</h1>
      </header>
      <main>
         <TodoList />
      </main>
    </div>
  )
}

export default App;
